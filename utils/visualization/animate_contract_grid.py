#!/usr/bin/env python3
"""
Animate one-at-a-time contractions of a directed M x N grid lattice.

This script imports the previous script as:

    import visualizer as vz

So put this file next to visualizer.py.

It does this:

  1. Build the whole list of contraction arrows at the outset.
  2. Optionally shuffle that list.
  3. Contract arrows one at a time.
  4. At frame k, draw the image after the first k contractions.
  5. Save as GIF or MP4.

Examples:

  python animate_contract_grid.py 20 30 --ratio 0.05 --seed 3 --out contraction.gif

  python animate_contract_grid.py 20 30 --ratio 1.0 --seed 3 --out full_contraction.gif

  python animate_contract_grid.py 20 30 --wrap --ratio 0.1 --seed 3 --out wrapped.mp4
"""

import argparse
import math
import random
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter

import visualizer as vz


def choose_number_of_hits(expected_hits, rng):
    """
    Same hit/miss logic as before.

    If expected_hits < 1:
      expected_hits = 0.3 gives one hit with probability 0.3
      and zero hits with probability 0.7.
    """
    base = math.floor(expected_hits)
    frac = expected_hits - base

    hits = base
    if rng.random() < frac:
        hits += 1

    return hits


def build_arrow_list(M, N, rng, wrap=False, ratio=1.0, shuffle=True):
    """
    Build the entire contraction-arrow list at the outset.

    Each eligible node contributes at most one arrow.
    ratio controls how many eligible nodes are activated.
    """
    if not (0.0 <= ratio <= 1.0):
        raise ValueError("--ratio must be between 0 and 1.")

    eligible = []

    for node in vz.grid_nodes(M, N):
        choices = vz.out_edges(node, M, N, wrap)
        if choices:
            eligible.append((node, choices))

    expected_hits = ratio * len(eligible)
    hit_count = choose_number_of_hits(expected_hits, rng)
    hit_count = min(hit_count, len(eligible))

    chosen_sources = rng.sample(eligible, hit_count)

    arrows = []
    for _node, choices in chosen_sources:
        arrows.append(rng.choice(choices))

    if shuffle:
        rng.shuffle(arrows)

    return arrows, len(eligible), expected_hits, hit_count


def is_short_display_edge(u, v):
    """
    Hide long wraparound arrows in the left-panel embedding.
    They are still contracted algebraically.
    """
    p = vz.node_xy(u)
    q = vz.node_xy(v)
    return abs(p[0] - q[0]) <= 1 and abs(p[1] - q[1]) <= 1


def draw_arrow_list_panel(ax, M, N, all_edges, arrows, active_count, dsu, components):
    """
    Left panel:
      - gray grid
      - pending arrows faint
      - already-contracted arrows dark
      - current arrow emphasized
    """
    vz.draw_original_grid(ax, M, N, all_edges)

    colors = vz.color_map(sorted(components.keys(), key=str))

    active_arrows = arrows[:active_count]
    pending_arrows = arrows[active_count:]

    # Pending arrows: faint.
    for u, v in pending_arrows:
        if not is_short_display_edge(u, v):
            continue

        p = vz.node_xy(u)
        q = vz.node_xy(v)

        vz.draw_arrow(
            ax,
            p,
            q,
            color="0.65",
            alpha=0.25,
            lw=1.0,
            zorder=2,
        )

    # Already collapsed arrows.
    for u, v in active_arrows:
        if not is_short_display_edge(u, v):
            continue

        p = vz.node_xy(u)
        q = vz.node_xy(v)
        root = dsu.find(u)

        vz.draw_arrow(
            ax,
            p,
            q,
            color=colors[root],
            alpha=0.95,
            lw=2.0,
            zorder=3,
        )

    # Current/latest arrow.
    if active_count > 0:
        u, v = arrows[active_count - 1]

        if is_short_display_edge(u, v):
            p = vz.node_xy(u)
            q = vz.node_xy(v)

            vz.draw_arrow(
                ax,
                p,
                q,
                color="black",
                alpha=1.0,
                lw=3.2,
                zorder=5,
            )

    ax.set_title(f"contractions applied: {active_count} / {len(arrows)}")
    ax.set_aspect("equal")
    ax.axis("off")


def state_after_k_contractions(nodes, all_edges, arrows, k):
    active_arrows = arrows[:k]

    dsu, components = vz.contract_edges(nodes, active_arrows)
    quotient_edges = vz.aggregate_quotient_edges(all_edges, dsu)

    return dsu, components, quotient_edges


def make_animation(args):
    rng = random.Random(args.seed)

    nodes = vz.grid_nodes(args.M, args.N)
    all_edges = vz.all_directed_grid_edges(args.M, args.N, args.wrap)

    arrows, eligible_count, expected_hits, hit_count = build_arrow_list(
        args.M,
        args.N,
        rng,
        wrap=args.wrap,
        ratio=args.ratio,
        shuffle=not args.no_shuffle,
    )

    if args.include_initial:
        frames = list(range(0, len(arrows) + 1))
    else:
        frames = list(range(1, len(arrows) + 1))

    if not frames:
        frames = [0]

    if args.max_frames is not None and len(frames) > args.max_frames:
        # Sample frames uniformly, while keeping the last frame.
        indices = [
            round(i * (len(frames) - 1) / (args.max_frames - 1))
            for i in range(args.max_frames)
        ]
        frames = [frames[i] for i in indices]

    fig, axes = plt.subplots(1, 2, figsize=(13, 6), constrained_layout=True)

    dim = eligible_count
    threshold = 1.0 / dim if dim else float("inf")

    if expected_hits < 1:
        hitmiss = "HIT" if hit_count else "MISS"
    else:
        hitmiss = None

    def update(k):
        for ax in axes:
            ax.clear()

        dsu, components, quotient_edges = state_after_k_contractions(
            nodes,
            all_edges,
            arrows,
            k,
        )

        draw_arrow_list_panel(
            axes[0],
            args.M,
            args.N,
            all_edges,
            arrows,
            k,
            dsu,
            components,
        )

        vz.draw_quotient(
            axes[1],
            components,
            quotient_edges,
        )

        title = (
            f"{args.M} x {args.N} directed grid"
            f" | ratio={args.ratio:g}"
            f" | 1/dim={threshold:g}"
            f" | chosen={hit_count}"
            f" | frame contractions={k}"
        )

        if args.wrap:
            title += " | wrap"

        if args.seed is not None:
            title += f" | seed={args.seed}"

        if hitmiss is not None:
            title += f" | {hitmiss}"

        fig.suptitle(title, fontsize=12)

        return axes

    anim = FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=1000 / args.fps,
        blit=False,
        repeat=args.repeat,
    )

    out = Path(args.out)
    suffix = out.suffix.lower()

    if suffix == ".gif":
        writer = PillowWriter(fps=args.fps)
    elif suffix == ".mp4":
        writer = FFMpegWriter(fps=args.fps)
    else:
        raise ValueError("Output must end in .gif or .mp4")

    anim.save(str(out), writer=writer, dpi=args.dpi)

    plt.close(fig)

    if expected_hits < 1:
        print(f"{hitmiss}: expected_hits={expected_hits:.6g}, actual_hits={hit_count}")

    print(f"eligible_nodes/dim = {dim}")
    print(f"1/dim = {threshold:.6g}")
    print(f"ratio = {args.ratio:.6g}")
    print(f"chosen contraction arrows = {hit_count}")
    print(f"animation frames = {len(frames)}")
    print(f"saved {out}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("M", type=int, help="number of grid rows")
    parser.add_argument("N", type=int, help="number of grid columns")

    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--wrap", action="store_true", help="use periodic boundary conditions")

    parser.add_argument(
        "--ratio",
        type=float,
        default=1.0,
        help="fraction of eligible nodes whose outgoing arrow enters the initial arrow list",
    )

    parser.add_argument(
        "--no-shuffle",
        action="store_true",
        help="do not shuffle the initial arrow list before collapsing one at a time",
    )

    parser.add_argument(
        "--include-initial",
        action="store_true",
        help="include frame 0 before any contractions",
    )

    parser.add_argument(
        "--max-frames",
        type=int,
        default=None,
        help="uniformly subsample the animation to at most this many frames",
    )

    parser.add_argument("--fps", type=int, default=12)
    parser.add_argument("--dpi", type=int, default=160)
    parser.add_argument("--repeat", action="store_true")
    parser.add_argument("--out", default="grid_contraction.gif")

    args = parser.parse_args()

    if args.M <= 0 or args.N <= 0:
        raise ValueError("M and N must be positive.")

    if args.fps <= 0:
        raise ValueError("--fps must be positive.")

    if args.max_frames is not None and args.max_frames < 2:
        raise ValueError("--max-frames must be at least 2.")

    make_animation(args)


if __name__ == "__main__":
    main()