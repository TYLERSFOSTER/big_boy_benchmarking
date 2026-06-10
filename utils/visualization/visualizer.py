#!/usr/bin/env python3
"""
Randomly contract outgoing edges in an M x N directed grid.

Convention:
  nodes are (row, col)
  outgoing edges point East and South:
      (r, c) -> (r, c + 1)
      (r, c) -> (r + 1, c)

New:
  --ratio controls the expected fraction of eligible nodes that contract.

If ratio * eligible_nodes < 1, the script performs a hit/miss:
  hit  -> one contraction
  miss -> zero contractions

Examples:
  python contract_grid.py 20 30 --ratio 1.0 --seed 4 --out full.png
  python contract_grid.py 20 30 --ratio 0.01 --seed 4 --out sparse.png
  python contract_grid.py 20 30 --ratio 0.0005 --seed 4 --out sub_one.png
"""

import argparse
import math
import random
from collections import defaultdict

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


class DSU:
    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.size = {x: 1 for x in items}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]


def grid_nodes(M, N):
    return [(r, c) for r in range(M) for c in range(N)]


def out_edges(v, M, N, wrap=False):
    r, c = v
    edges = []

    if c + 1 < N:
        edges.append((v, (r, c + 1)))
    elif wrap:
        edges.append((v, (r, 0)))

    if r + 1 < M:
        edges.append((v, (r + 1, c)))
    elif wrap:
        edges.append((v, (0, c)))

    return edges


def all_directed_grid_edges(M, N, wrap=False):
    edges = []
    for v in grid_nodes(M, N):
        edges.extend(out_edges(v, M, N, wrap))
    return edges


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


def choose_contractions(M, N, rng, wrap=False, ratio=1.0):
    """
    Choose a sparse random subset of contraction edges.

    ratio = 1.0 means every eligible node chooses one outgoing edge.
    ratio = 0.1 means about 10% of eligible nodes choose one outgoing edge.
    ratio < 1 / eligible_nodes gives a Bernoulli hit/miss for one edge.
    """
    eligible = []

    for v in grid_nodes(M, N):
        choices = out_edges(v, M, N, wrap)
        if choices:
            eligible.append((v, choices))

    if not (0.0 <= ratio <= 1.0):
        raise ValueError("--ratio must be between 0 and 1.")

    expected_hits = ratio * len(eligible)
    hit_count = choose_number_of_hits(expected_hits, rng)
    hit_count = min(hit_count, len(eligible))

    chosen_sources = rng.sample(eligible, hit_count)

    chosen_edges = []
    for _v, choices in chosen_sources:
        chosen_edges.append(rng.choice(choices))

    return chosen_edges, len(eligible), expected_hits, hit_count


def contract_edges(nodes, chosen_edges):
    dsu = DSU(nodes)

    for u, v in chosen_edges:
        dsu.union(u, v)

    components = defaultdict(list)
    for v in nodes:
        components[dsu.find(v)].append(v)

    return dsu, components


def node_xy(v):
    r, c = v
    return c, -r


def component_centroids(components):
    centroids = {}
    for root, verts in components.items():
        xs, ys = zip(*(node_xy(v) for v in verts))
        centroids[root] = (sum(xs) / len(xs), sum(ys) / len(ys))
    return centroids


def aggregate_quotient_edges(all_edges, dsu):
    mult = defaultdict(int)

    for u, v in all_edges:
        ru, rv = dsu.find(u), dsu.find(v)
        if ru != rv:
            mult[(ru, rv)] += 1

    return mult


def color_map(keys):
    cmap = plt.get_cmap("tab20")
    return {k: cmap(i % 20) for i, k in enumerate(keys)}


def draw_arrow(ax, p, q, color="black", alpha=1.0, lw=1.0, rad=0.0, zorder=1):
    arrow = FancyArrowPatch(
        p,
        q,
        arrowstyle="-|>",
        mutation_scale=9,
        linewidth=lw,
        color=color,
        alpha=alpha,
        connectionstyle=f"arc3,rad={rad}",
        shrinkA=3,
        shrinkB=3,
        zorder=zorder,
    )
    ax.add_patch(arrow)


def draw_original_grid(ax, M, N, all_edges):
    for u, v in all_edges:
        x1, y1 = node_xy(u)
        x2, y2 = node_xy(v)

        # Avoid long wraparound edges through the middle of the picture.
        if abs(x1 - x2) > 1 or abs(y1 - y2) > 1:
            continue

        ax.plot([x1, x2], [y1, y2], color="0.86", lw=0.7, zorder=0)

    xs, ys = zip(*(node_xy(v) for v in grid_nodes(M, N)))
    ax.scatter(xs, ys, s=8, color="0.55", zorder=2)


def draw_chosen_contraction_forest(ax, M, N, all_edges, chosen_edges, dsu, components):
    colors = color_map(sorted(components.keys(), key=str))
    draw_original_grid(ax, M, N, all_edges)

    for u, v in chosen_edges:
        p = node_xy(u)
        q = node_xy(v)

        # Skip long wraparound display edges.
        if abs(p[0] - q[0]) > 1 or abs(p[1] - q[1]) > 1:
            continue

        root = dsu.find(u)
        draw_arrow(ax, p, q, color=colors[root], alpha=0.95, lw=2.2, zorder=3)

    ax.set_title("chosen contraction hits")
    ax.set_aspect("equal")
    ax.axis("off")


def draw_quotient(ax, components, quotient_edges):
    roots = list(components.keys())
    centroids = component_centroids(components)
    colors = color_map(sorted(roots, key=str))

    if len(roots) == 1:
        root = roots[0]
        x, y = centroids[root]
        ax.scatter([x], [y], s=900, color=colors[root], edgecolor="black", linewidth=1.5)
        ax.text(
            x,
            y,
            f"{len(components[root])} nodes\ncollapsed",
            ha="center",
            va="center",
            fontsize=10,
        )
        ax.set_title("quotient: one component")
        ax.set_aspect("equal")
        ax.axis("off")
        return

    for i, ((a, b), count) in enumerate(quotient_edges.items()):
        p = centroids[a]
        q = centroids[b]
        rad = 0.10 if i % 2 == 0 else -0.10
        lw = 0.4 + 0.25 * min(count, 8)
        draw_arrow(ax, p, q, color="0.25", alpha=0.35, lw=lw, rad=rad, zorder=1)

    for root, verts in components.items():
        x, y = centroids[root]
        size = 20 + 12 * len(verts)

        ax.scatter(
            [x],
            [y],
            s=size,
            color=colors[root],
            edgecolor="black",
            linewidth=0.5,
            zorder=3,
        )

        if len(verts) > 1:
            ax.text(x, y, str(len(verts)), ha="center", va="center", fontsize=7, zorder=4)

    ax.set_title("quotient after sparse contractions")
    ax.set_aspect("equal")
    ax.axis("off")


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
        help="fraction of eligible nodes that contract; may be below 1/dim",
    )
    parser.add_argument("--out", default="grid_contraction.png")
    parser.add_argument("--dpi", type=int, default=220)
    args = parser.parse_args()

    if args.M <= 0 or args.N <= 0:
        raise ValueError("M and N must be positive.")

    rng = random.Random(args.seed)

    nodes = grid_nodes(args.M, args.N)
    all_edges = all_directed_grid_edges(args.M, args.N, args.wrap)

    chosen_edges, eligible_count, expected_hits, hit_count = choose_contractions(
        args.M,
        args.N,
        rng,
        wrap=args.wrap,
        ratio=args.ratio,
    )

    dsu, components = contract_edges(nodes, chosen_edges)
    quotient_edges = aggregate_quotient_edges(all_edges, dsu)

    fig, axes = plt.subplots(1, 2, figsize=(13, 6), constrained_layout=True)

    draw_chosen_contraction_forest(
        axes[0],
        args.M,
        args.N,
        all_edges,
        chosen_edges,
        dsu,
        components,
    )

    draw_quotient(axes[1], components, quotient_edges)

    dim = eligible_count
    threshold = 1.0 / dim if dim else float("inf")

    title = (
        f"{args.M} x {args.N} directed grid"
        f" | ratio={args.ratio:g}"
        f" | 1/dim={threshold:g}"
        f" | hits={hit_count}"
        f" | expected={expected_hits:.3g}"
    )

    if args.wrap:
        title += " | wrap"

    if args.seed is not None:
        title += f" | seed={args.seed}"

    fig.suptitle(title, fontsize=12)

    fig.savefig(args.out, dpi=args.dpi, bbox_inches="tight")

    if expected_hits < 1:
        result = "HIT" if hit_count else "MISS"
        print(f"{result}: expected_hits={expected_hits:.6g}, actual_hits={hit_count}")

    print(f"eligible_nodes/dim = {dim}")
    print(f"1/dim = {threshold:.6g}")
    print(f"ratio = {args.ratio:.6g}")
    print(f"chosen contractions = {hit_count}")
    print(f"saved {args.out}")


if __name__ == "__main__":
    main()