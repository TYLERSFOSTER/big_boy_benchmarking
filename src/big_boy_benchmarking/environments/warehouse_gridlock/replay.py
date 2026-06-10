"""Episode replay rendering for Warehouse Gridlock artifacts."""

from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from textwrap import shorten
from typing import Any

from PIL import Image, ImageDraw, ImageFont

from big_boy_benchmarking.environments.warehouse_gridlock.graph import GridNode
from big_boy_benchmarking.environments.warehouse_gridlock.ids import (
    WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID,
)
from big_boy_benchmarking.environments.warehouse_gridlock.instances import load_instance
from big_boy_benchmarking.environments.warehouse_gridlock.state import (
    WarehouseGridlockState,
)


@dataclass(frozen=True)
class EpisodeReplayResult:
    status: str
    output_path: Path
    step_events_path: Path
    run_id: str
    arm_id: str
    episode_index: int
    frame_count: int
    row_count: int
    state_trajectory_hash: str
    action_trajectory_hash: str

    def to_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "output_path": str(self.output_path),
            "step_events_path": str(self.step_events_path),
            "run_id": self.run_id,
            "arm_id": self.arm_id,
            "episode_index": self.episode_index,
            "frame_count": self.frame_count,
            "row_count": self.row_count,
            "state_trajectory_hash": self.state_trajectory_hash,
            "action_trajectory_hash": self.action_trajectory_hash,
        }


def render_episode_gif(
    *,
    episode_index: int,
    output_path: Path | None = None,
    step_events_path: Path | None = None,
    artifact_root: Path | None = None,
    run_id: str | None = None,
    arm_id: str | None = None,
    replicate_index: int | None = None,
    schema_seed: int | None = None,
    instance_id: str = WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID,
    frame_ms: int = 140,
    cell_pixels: int = 36,
    max_frames: int | None = None,
) -> EpisodeReplayResult:
    resolved_step_events = resolve_step_events_path(
        artifact_root=artifact_root,
        step_events_path=step_events_path,
        run_id=run_id,
        arm_id=arm_id,
        replicate_index=replicate_index,
        schema_seed=schema_seed,
    )
    rows = _episode_rows(resolved_step_events, episode_index)
    if not rows:
        raise ValueError(
            f"no rows for episode_index={episode_index} in {resolved_step_events}"
        )

    instance = load_instance(instance_id=instance_id)
    frame_payloads = _frame_payloads(rows, max_frames=max_frames)
    frames = [
        _render_frame(
            state=parse_state_id(payload["state_id"]),
            instance=instance,
            episode_index=episode_index,
            frame_number=frame_number,
            total_frames=len(frame_payloads),
            row=payload.get("row"),
            cell_pixels=cell_pixels,
        )
        for frame_number, payload in enumerate(frame_payloads)
    ]
    if not frames:
        raise ValueError("episode replay produced no frames")

    target = output_path or _default_output_path(
        artifact_root=artifact_root,
        step_events_path=resolved_step_events,
        run_id=str(rows[0]["run_id"]),
        arm_id=str(rows[0]["arm_id"]),
        replicate_index=int(rows[0]["replicate_index"]),
        schema_seed=int(rows[0]["schema_seed"]),
        episode_index=episode_index,
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        target,
        save_all=True,
        append_images=frames[1:],
        duration=frame_ms,
        loop=0,
        optimize=False,
    )
    return EpisodeReplayResult(
        status="success",
        output_path=target,
        step_events_path=resolved_step_events,
        run_id=str(rows[0]["run_id"]),
        arm_id=str(rows[0]["arm_id"]),
        episode_index=episode_index,
        frame_count=len(frames),
        row_count=len(rows),
        state_trajectory_hash=_state_trajectory_hash(rows),
        action_trajectory_hash=_action_trajectory_hash(rows),
    )


def resolve_step_events_path(
    *,
    artifact_root: Path | None,
    step_events_path: Path | None,
    run_id: str | None,
    arm_id: str | None,
    replicate_index: int | None,
    schema_seed: int | None,
) -> Path:
    if step_events_path is not None:
        path = Path(step_events_path)
        if not path.exists():
            raise FileNotFoundError(f"step_events path does not exist: {path}")
        return path
    if artifact_root is None:
        raise ValueError("provide either --step-events or --artifact-root")

    root = Path(artifact_root)
    if run_id:
        path = root / "runs" / run_id / "step_events.csv"
        if not path.exists():
            raise FileNotFoundError(f"step_events path does not exist: {path}")
        return path

    run_index = root / "run_index.csv"
    if not run_index.exists():
        raise FileNotFoundError(f"run_index.csv does not exist: {run_index}")
    matches = _matching_run_index_rows(
        run_index,
        arm_id=arm_id,
        replicate_index=replicate_index,
        schema_seed=schema_seed,
    )
    if not matches:
        raise ValueError(
            "no run_index.csv row matched "
            f"arm_id={arm_id!r}, replicate_index={replicate_index!r}, "
            f"schema_seed={schema_seed!r}"
        )
    if len(matches) > 1:
        choices = ", ".join(row["run_id"] for row in matches[:5])
        raise ValueError(
            "run selector matched multiple rows; add --run-id, --arm-id, "
            "--replicate-index, or --schema-seed. "
            f"First matches: {choices}"
        )
    row = matches[0]
    candidates = _candidate_step_event_paths(root=root, row=row)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "matched run_index.csv row, but no step_events.csv exists for "
        f"run_id={row['run_id']}"
    )


def parse_state_id(state_id: str) -> WarehouseGridlockState:
    pieces = state_id.split("|")
    if len(pieces) != 3 or not pieces[0].startswith("t"):
        raise ValueError(f"unsupported Warehouse state id: {state_id}")
    time_step = int(pieces[0][1:])
    robots = _parse_entity_positions(pieces[1], "robots")
    boxes = _parse_entity_positions(pieces[2], "boxes")
    return WarehouseGridlockState(
        robot_positions=robots,
        box_positions=boxes,
        time_step=time_step,
    )


def _matching_run_index_rows(
    run_index: Path,
    *,
    arm_id: str | None,
    replicate_index: int | None,
    schema_seed: int | None,
) -> list[dict[str, str]]:
    with run_index.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    matches = []
    for row in rows:
        if arm_id is not None and row.get("arm_id") != arm_id:
            continue
        if replicate_index is not None and int(row.get("replicate_index", "-1")) != replicate_index:
            continue
        if schema_seed is not None and int(row.get("schema_seed", "-1")) != schema_seed:
            continue
        matches.append(row)
    return matches


def _candidate_step_event_paths(*, root: Path, row: dict[str, str]) -> list[Path]:
    candidates: list[Path] = []
    run_root_text = row.get("run_root", "")
    if run_root_text:
        run_root = Path(run_root_text)
        if run_root.is_absolute():
            candidates.append(run_root / "step_events.csv")
        else:
            candidates.append(run_root / "step_events.csv")
            for ancestor in root.parents:
                candidates.append(ancestor / run_root / "step_events.csv")
    candidates.append(root / "runs" / row["run_id"] / "step_events.csv")
    return _unique_paths(candidates)


def _unique_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    unique: list[Path] = []
    for path in paths:
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        unique.append(path)
    return unique


def _episode_rows(step_events_path: Path, episode_index: int) -> list[dict[str, str]]:
    with step_events_path.open(newline="", encoding="utf-8") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if int(row["episode_index"]) == episode_index
        ]
    return sorted(rows, key=lambda row: int(row["step_index"]))


def _frame_payloads(
    rows: list[dict[str, str]],
    *,
    max_frames: int | None,
) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = [{"state_id": rows[0]["state_id"]}]
    for row in rows:
        payloads.append({"state_id": row["next_state_id"], "row": row})
    if max_frames is not None:
        if max_frames <= 0:
            raise ValueError("max_frames must be positive when provided")
        return payloads[:max_frames]
    return payloads


def _parse_entity_positions(piece: str, prefix: str) -> dict[str, GridNode]:
    expected = f"{prefix}="
    if not piece.startswith(expected):
        raise ValueError(f"expected {expected!r} in state id piece: {piece}")
    entity_blob = piece[len(expected) :]
    positions: dict[str, GridNode] = {}
    if not entity_blob:
        return positions
    for item in entity_blob.split(","):
        entity_id, node_key = item.split(":", 1)
        positions[entity_id] = _parse_node_key(node_key)
    return positions


def _parse_node_key(node_key: str) -> GridNode:
    match = re.fullmatch(r"r(\d+)c(\d+)", node_key)
    if match is None:
        raise ValueError(f"unsupported grid node key: {node_key}")
    return GridNode(row=int(match.group(1)), col=int(match.group(2)))


def _render_frame(
    *,
    state: WarehouseGridlockState,
    instance: Any,
    episode_index: int,
    frame_number: int,
    total_frames: int,
    row: dict[str, str] | None,
    cell_pixels: int,
) -> Image.Image:
    manifest = instance.manifest
    rows = manifest.grid.rows
    cols = manifest.grid.cols
    grid_left = 44
    grid_top = 82
    right_pad = 28
    bottom_pad = 34
    width = grid_left + cols * cell_pixels + right_pad
    height = grid_top + rows * cell_pixels + bottom_pad
    image = Image.new("RGB", (width, height), (248, 250, 252))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    _draw_header(
        draw=draw,
        font=font,
        width=width,
        state=state,
        episode_index=episode_index,
        frame_number=frame_number,
        total_frames=total_frames,
        row=row,
    )
    _draw_targets(
        draw=draw,
        manifest=manifest,
        grid_left=grid_left,
        grid_top=grid_top,
        cell_pixels=cell_pixels,
    )
    _draw_blocked_nodes(
        draw=draw,
        blocked_nodes=instance.graph.blocked_nodes,
        grid_left=grid_left,
        grid_top=grid_top,
        cell_pixels=cell_pixels,
    )
    _draw_grid(
        draw=draw,
        rows=rows,
        cols=cols,
        grid_left=grid_left,
        grid_top=grid_top,
        cell_pixels=cell_pixels,
    )
    _draw_boxes(
        draw=draw,
        box_positions=state.box_positions,
        grid_left=grid_left,
        grid_top=grid_top,
        cell_pixels=cell_pixels,
        font=font,
    )
    _draw_robots(
        draw=draw,
        robot_positions=state.robot_positions,
        grid_left=grid_left,
        grid_top=grid_top,
        cell_pixels=cell_pixels,
        font=font,
    )
    return image


def _draw_header(
    *,
    draw: ImageDraw.ImageDraw,
    font: ImageFont.ImageFont,
    width: int,
    state: WarehouseGridlockState,
    episode_index: int,
    frame_number: int,
    total_frames: int,
    row: dict[str, str] | None,
) -> None:
    title = f"Warehouse Gridlock replay | episode={episode_index} | t={state.time_step}"
    detail = f"frame {frame_number + 1}/{total_frames}"
    if row is not None:
        detail += (
            f" | step={row['step_index']} | reward={row['reward']} | "
            f"boxes={row['correct_box_count']} robots={row['correct_robot_count']}"
        )
    action = "initial state" if row is None else row.get("selected_action_summary", "")
    draw.text((16, 14), title, fill=(15, 23, 42), font=font)
    draw.text((16, 34), detail, fill=(51, 65, 85), font=font)
    draw.text(
        (16, 54),
        shorten(f"action: {action}", width=max(48, width // 7), placeholder="..."),
        fill=(71, 85, 105),
        font=font,
    )


def _draw_grid(
    *,
    draw: ImageDraw.ImageDraw,
    rows: int,
    cols: int,
    grid_left: int,
    grid_top: int,
    cell_pixels: int,
) -> None:
    grid_color = (203, 213, 225)
    for row in range(rows + 1):
        y = grid_top + row * cell_pixels
        draw.line((grid_left, y, grid_left + cols * cell_pixels, y), fill=grid_color)
    for col in range(cols + 1):
        x = grid_left + col * cell_pixels
        draw.line((x, grid_top, x, grid_top + rows * cell_pixels), fill=grid_color)


def _draw_targets(
    *,
    draw: ImageDraw.ImageDraw,
    manifest: Any,
    grid_left: int,
    grid_top: int,
    cell_pixels: int,
) -> None:
    for target in manifest.box_targets:
        x0, y0, x1, y1 = _cell_rect(
            target.target,
            grid_left=grid_left,
            grid_top=grid_top,
            cell_pixels=cell_pixels,
            inset=4,
        )
        draw.rectangle((x0, y0, x1, y1), outline=(234, 88, 12), width=2)
    for target in manifest.robot_targets:
        x0, y0, x1, y1 = _cell_rect(
            target.target,
            grid_left=grid_left,
            grid_top=grid_top,
            cell_pixels=cell_pixels,
            inset=8,
        )
        draw.ellipse((x0, y0, x1, y1), outline=(37, 99, 235), width=2)


def _draw_blocked_nodes(
    *,
    draw: ImageDraw.ImageDraw,
    blocked_nodes: frozenset[GridNode],
    grid_left: int,
    grid_top: int,
    cell_pixels: int,
) -> None:
    for node in blocked_nodes:
        x0, y0, x1, y1 = _cell_rect(
            node,
            grid_left=grid_left,
            grid_top=grid_top,
            cell_pixels=cell_pixels,
            inset=1,
        )
        draw.rectangle((x0, y0, x1, y1), fill=(71, 85, 105), outline=(30, 41, 59))


def _draw_boxes(
    *,
    draw: ImageDraw.ImageDraw,
    box_positions: Any,
    grid_left: int,
    grid_top: int,
    cell_pixels: int,
    font: ImageFont.ImageFont,
) -> None:
    for box_id, node in sorted(box_positions.items()):
        x0, y0, x1, y1 = _cell_rect(
            node,
            grid_left=grid_left,
            grid_top=grid_top,
            cell_pixels=cell_pixels,
            inset=5,
        )
        draw.rectangle((x0, y0, x1, y1), fill=(245, 158, 11), outline=(146, 64, 14))
        _draw_centered_label(draw, (x0, y0, x1, y1), box_id, font, fill=(67, 20, 7))


def _draw_robots(
    *,
    draw: ImageDraw.ImageDraw,
    robot_positions: Any,
    grid_left: int,
    grid_top: int,
    cell_pixels: int,
    font: ImageFont.ImageFont,
) -> None:
    for robot_id, node in sorted(robot_positions.items()):
        x0, y0, x1, y1 = _cell_rect(
            node,
            grid_left=grid_left,
            grid_top=grid_top,
            cell_pixels=cell_pixels,
            inset=7,
        )
        draw.ellipse((x0, y0, x1, y1), fill=(59, 130, 246), outline=(30, 64, 175))
        _draw_centered_label(draw, (x0, y0, x1, y1), robot_id, font, fill=(255, 255, 255))


def _cell_rect(
    node: GridNode,
    *,
    grid_left: int,
    grid_top: int,
    cell_pixels: int,
    inset: int,
) -> tuple[int, int, int, int]:
    x0 = grid_left + (node.col - 1) * cell_pixels + inset
    y0 = grid_top + (node.row - 1) * cell_pixels + inset
    x1 = grid_left + node.col * cell_pixels - inset
    y1 = grid_top + node.row * cell_pixels - inset
    return x0, y0, x1, y1


def _draw_centered_label(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    label: str,
    font: ImageFont.ImageFont,
    *,
    fill: tuple[int, int, int],
) -> None:
    x0, y0, x1, y1 = rect
    short_label = label[-2:] if len(label) > 2 else label
    bbox = draw.textbbox((0, 0), short_label, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    draw.text(
        (
            x0 + ((x1 - x0) - text_width) / 2,
            y0 + ((y1 - y0) - text_height) / 2,
        ),
        short_label,
        fill=fill,
        font=font,
    )


def _default_output_path(
    *,
    artifact_root: Path | None,
    step_events_path: Path,
    run_id: str,
    arm_id: str,
    replicate_index: int,
    schema_seed: int,
    episode_index: int,
) -> Path:
    safe_arm = _safe_slug(arm_id)
    filename = (
        f"{safe_arm}-rep{replicate_index}-schema{schema_seed}"
        f"-episode{episode_index:03d}.gif"
    )
    if artifact_root is not None:
        return Path(artifact_root) / "replays" / filename
    return step_events_path.parent / "replays" / filename


def _safe_slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-") or "episode"


def _state_trajectory_hash(rows: list[dict[str, str]]) -> str:
    states = [rows[0]["state_id"]]
    states.extend(row["next_state_id"] for row in rows)
    return hashlib.sha256("\n".join(states).encode("utf-8")).hexdigest()


def _action_trajectory_hash(rows: list[dict[str, str]]) -> str:
    actions = [row["selected_action_id"] for row in rows]
    return hashlib.sha256("\n".join(actions).encode("utf-8")).hexdigest()
