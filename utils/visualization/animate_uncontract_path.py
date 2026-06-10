#!/usr/bin/env python3
"""
Animate reverse one-at-a-time uncontractions of a directed M x N grid lattice,
and overlay one dark NW-to-SE path on the quotient graph at every tier.

This imports the previous static visualizer script as:

    import visualizer as vz

So put this file next to visualizer.py.

The arrow list is built in the same way as animate_contract_grid.py:

  1. Build the whole list of contraction arrows at the outset.
  2. Optionally shuffle that list.
  3. Start with all chosen arrows contracted.
  4. Remove/uncontract arrows one at a time, in reverse order.
  5. At each quotient tier, draw all quotient edges faintly as before.
  6. Overlay one extra-dark, bold NW-to-SE path.

Important convention:
  The grid arrows point East and South, but a NW-to-SE path needs to move
  West/South. So the highlighted path is computed in the underlying
  undirected quotient graph. The dark arrowheads show traversal from NW to SE;
  they are a path overlay, not a claim that the original edge orientation agrees.

Examples:

  python animate_uncontract_path.py 20 30 --ratio 0.05 --seed 3 --out uncontract_path.gif

  python animate_uncontract_path.py 20 30 --ratio 1.0 --seed 3 \
      --max-frames 180 --out full_uncontract_path.gif

  python animate_uncontract_path.py 20 30 --wrap --ratio 0.1 --seed 3 \
      --out wrapped_uncontract_path.mp4
"""

import argparse
import math
import random
from collections import deque
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter

import visualizer as vz


# -----------------------------------------------------------------------------
# Same arrow-list generation logic as the forward animation script.
# -----------------------------------------------------------------------------


def choose_number_of_hits(expected_hits, rng):
    """
    Convert a possibly fractional expected number of contractions into
    an integer count.

    Examples:
      expected_hits = 17.3 -> 17 or 18
      expected_hits = 0.2  -> 0 or 1
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


# -----------------------------------------------------------------------------
# Quotient states.
# -----------------------------------------------------------------------------


def state_after_k_contractions(nodes, all_edges, arrows, k):
    """
    k = number of arrows still contracted.

    In the reverse movie, k starts at len(arrows) and decreases to 0.
    """
    active_arrows = arrows[:k]

    dsu, components = vz.contract_edges(nodes, active_arrows)
    quotient_edges = vz.aggregate_quotient_edges(all_edges, dsu)

    return dsu, components, quotient_edges


def northwest_node(M, N):
    return (0, 0)


def southeast_node(M, N):
    return (M - 1, N - 1)


def quotient_endpoints(M, N, dsu):
    """
    Use actual grid corners as path endpoints, then pass to their current
    quotient components.
    """
    start = dsu.find(northwest_node(M, N))
    goal = dsu.find(southeast_node(M, N))
    return start, goal


def undirected_adjacency(components, quotient_edges):
    """
    The quotient itself is directed, but the highlighted NW-to-SE route is
    drawn as a path in the underlying undirected graph.
    """
    adj = {root: set() for root in components}

    for a, b in quotient_edges:
        if a == b:
            continue
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)

    return adj


# -----------------------------------------------------------------------------
# Random path + gap-closing repair.
# -----------------------------------------------------------------------------


def compress_consecutive(path):
    out = []
    for x in path:
        if not out or out[-1] != x:
            out.append(x)
    return out


def loop_erase_walk(walk):
    """
    Turn a possibly loopy repaired walk into a simple path by chronological
    loop erasure.
    """
    out = []
    position = {}

    for node in walk:
        if node in position:
            keep_through = position[node]
            out = out[: keep_through + 1]
            position = {v: i for i, v in enumerate(out)}
        else:
            position[node] = len(out)
            out.append(node)

    return out


def randomized_bfs_path(adj, start, goal, rng):
    """
    Return one random shortest path from start to goal in an undirected graph.
    Randomness only breaks ties among BFS choices.
    """
    if start == goal:
        return [start]

    q = deque([start])
    parent = {start: None}

    while q:
        u = q.popleft()
        neighbors = list(adj.get(u, ()))
        rng.shuffle(neighbors)

        for v in neighbors:
            if v in parent:
                continue

            parent[v] = u

            if v == goal:
                path = [goal]
                cur = goal
                while parent[cur] is not None:
                    cur = parent[cur]
                    path.append(cur)
                path.reverse()
                return path

            q.append(v)

    return None


def repair_projected_path(previous_path, dsu, adj, start, goal, rng):
    """
    Preserve the previous path where possible after an uncontraction.

    Mechanism:
      1. Project old quotient vertices into the new, less-contracted quotient.
      2. Consecutive projected vertices that are still adjacent stay connected.
      3. When a projected segment has disappeared, close that gap by choosing
         a random shortest bridge in the current quotient graph.

    This is the "random gap-closing choice" part.
    """
    if not previous_path or len(previous_path) < 2:
        return randomized_bfs_path(adj, start, goal, rng)

    projected = [dsu.find(root) for root in previous_path]
    targets = compress_consecutive([start] + projected + [goal])

    repaired = [targets[0]]

    for target in targets[1:]:
        current = repaired[-1]

        if current == target:
            continue

        if target in adj.get(current, set()):
            repaired.append(target)
            continue

        bridge = randomized_bfs_path(adj, current, target, rng)
        if bridge is None:
            return randomized_bfs_path(adj, start, goal, rng)

        repaired.extend(bridge[1:])

    repaired = loop_erase_walk(compress_consecutive(repaired))

    if not repaired or repaired[0] != start or repaired[-1] != goal:
        return randomized_bfs_path(adj, start, goal, rng)

    return repaired


# -----------------------------------------------------------------------------
# Drawing helpers.
# -----------------------------------------------------------------------------


def is_short_display_edge(u, v):
    """
    Hide long wraparound arrows in the left-panel embedding.
    They are still contracted/uncontracted algebraically.
    """
    p = vz.node_xy(u)
    q = vz.node_xy(v)
    return abs(p[0] - q[0]) <= 1 and abs(p[1] - q[1]) <= 1


def draw_uncontraction_panel(ax, M, N, all_edges, arrows, active_count, dsu, components):
    """
    Left panel:
      - gray original grid
      - arrows still contracted are colored
      - arrows already uncontracted are faint gray
      - most recently uncontracted arrow is dark gray
    """
    vz.draw_original_grid(ax, M, N, all_edges)

    colors = vz.color_map(sorted(components.keys(), key=str))

    active_arrows = arrows[:active_count]
    removed_arrows = arrows[active_count:]

    # Already uncontracted arrows: present only as ghost memory.
    for u, v in removed_arrows:
        if not is_short_display_edge(u, v):
            continue

        p = vz.node_xy(u)
        q = vz.node_xy(v)

        vz.draw_arrow(
            ax,
            p,
            q,
            color="0.70",
            alpha=0.14,
            lw=1.0,
            zorder=1,
        )

    # Still-contracted arrows.
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
            alpha=0.90,
            lw=2.0,
            zorder=3,
        )

    # Latest arrow removed in this reverse tier.
    if active_count < len(arrows):
        u, v = arrows[active_count]

        if is_short_display_edge(u, v):
            p = vz.node_xy(u)
            q = vz.node_xy(v)

            vz.draw_arrow(
                ax,
                p,
                q,
                color="0.10",
                alpha=0.45,
                lw=3.0,
                zorder=4,
            )

    ax.set_title(f"still contracted: {active_count} / {len(arrows)}")
    ax.set_aspect("equal")
    ax.axis("off")


def draw_path_overlay(ax, components, path, path_lw=4.6):
    """
    Draw exactly one extra-dark highlighted path on top of the existing
    quotient graph.
    """
    if not path:
        return

    centroids = vz.component_centroids(components)

    if len(path) == 1:
        root = path[0]
        if root in centroids:
            x, y = centroids[root]
            ax.scatter(
                [x],
                [y],
                s=260,
                facecolors="none",
                edgecolors="black",
                linewidths=2.2,
                zorder=8,
            )
        return

    for a, b in zip(path, path[1:]):
        if a not in centroids or b not in centroids:
            continue

        p = centroids[a]
        q = centroids[b]

        vz.draw_arrow(
            ax,
            p,
            q,
            color="black",
            alpha=0.98,
            lw=path_lw,
            rad=0.0,
            zorder=9,
        )


def draw_quotient_with_path(ax, components, quotient_edges, path):
    vz.draw_quotient(ax, components, quotient_edges)
    draw_path_overlay(ax, components, path)

    if path:
        ax.set_title(f"quotient with one bold NW-to-SE path | length {len(path) - 1}")
    else:
        ax.set_title("quotient with no NW-to-SE path found")


# -----------------------------------------------------------------------------
# Frame planning / animation.
# -----------------------------------------------------------------------------


def reverse_active_counts(num_arrows, max_frames=None):
    """
    Return active contraction counts for the reverse movie:
      num_arrows, num_arrows - 1, ..., 0
    """
    frames = list(range(num_arrows, -1, -1))

    if max_frames is not None and len(frames) > max_frames:
        if max_frames < 2:
            raise ValueError("--max-frames must be at least 2.")

        indices = [
            round(i * (len(frames) - 1) / (max_frames - 1))
            for i in range(max_frames)
        ]
        frames = [frames[i] for i in indices]

    return frames


def precompute_frame_data(args, nodes, all_edges, arrows, frames):
    """
    Precompute states and paths so animation saving cannot perturb the random
    path choices by calling update() more than once for a frame.
    """
    path_seed = args.path_seed if args.path_seed is not None else args.seed
    path_rng = random.Random(path_seed)

    previous_path = None
    data = []

    for k in frames:
        dsu, components, quotient_edges = state_after_k_contractions(
            nodes,
            all_edges,
            arrows,
            k,
        )

        start, goal = quotient_endpoints(args.M, args.N, dsu)
        adj = undirected_adjacency(components, quotient_edges)

        if args.fresh_path_each_frame:
            path = randomized_bfs_path(adj, start, goal, path_rng)
        else:
            path = repair_projected_path(previous_path, dsu, adj, start, goal, path_rng)

        if path is None:
            path = []

        previous_path = path

        data.append(
            {
                "active_count": k,
                "dsu": dsu,
                "components": components,
                "quotient_edges": quotient_edges,
                "path": path,
            }
        )

    return data


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

    frames = reverse_active_counts(len(arrows), args.max_frames)
    frame_data = precompute_frame_data(args, nodes, all_edges, arrows, frames)

    fig, axes = plt.subplots(1, 2, figsize=(13, 6), constrained_layout=True)

    dim = eligible_count
    threshold = 1.0 / dim if dim else float("inf")

    if expected_hits < 1:
        hitmiss = "HIT" if hit_count else "MISS"
    else:
        hitmiss = None

    def update(i):
        item = frame_data[i]

        for ax in axes:
            ax.clear()

        active_count = item["active_count"]
        dsu = item["dsu"]
        components = item["components"]
        quotient_edges = item["quotient_edges"]
        path = item["path"]

        draw_uncontraction_panel(
            axes[0],
            args.M,
            args.N,
            all_edges,
            arrows,
            active_count,
            dsu,
            components,
        )

        draw_quotient_with_path(
            axes[1],
            components,
            quotient_edges,
            path,
        )

        title = (
            f"reverse uncontraction | {args.M} x {args.N} directed grid"
            f" | ratio={args.ratio:g}"
            f" | 1/dim={threshold:g}"
            f" | chosen={hit_count}"
            f" | still contracted={active_count}"
        )

        if args.wrap:
            title += " | wrap"

        if args.seed is not None:
            title += f" | seed={args.seed}"

        if args.path_seed is not None:
            title += f" | path-seed={args.path_seed}"

        if hitmiss is not None:
            title += f" | {hitmiss}"

        fig.suptitle(title, fontsize=12)

        return axes

    anim = FuncAnimation(
        fig,
        update,
        frames=len(frame_data),
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
    print(f"animation frames = {len(frame_data)}")
    print(f"saved {out}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("M", type=int, help="number of grid rows")
    parser.add_argument("N", type=int, help="number of grid columns")

    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument(
        "--path-seed",
        type=int,
        default=None,
        help="separate seed for random path gap-closure choices; defaults to --seed",
    )
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
        help="do not shuffle the initial arrow list before reverse uncontraction",
    )

    parser.add_argument(
        "--fresh-path-each-frame",
        action="store_true",
        help="ignore previous path and choose a fresh random shortest NW-to-SE path each frame",
    )

    parser.add_argument(
        "--max-frames",
        type=int,
        default=None,
        help="uniformly subsample the reverse animation to at most this many frames",
    )

    parser.add_argument("--fps", type=int, default=12)
    parser.add_argument("--dpi", type=int, default=160)
    parser.add_argument("--repeat", action="store_true")
    parser.add_argument("--out", default="uncontract_path.gif")

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
