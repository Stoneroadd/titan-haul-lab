"""Reproducible synthetic haul-cycle scenario comparison."""

from __future__ import annotations

import argparse
import csv
import json
import random
import statistics
from pathlib import Path


def simulate(seed: int, cycles: int, queue_reduction: float) -> list[dict]:
    if cycles < 1 or not 0 <= queue_reduction <= 1:
        raise ValueError("cycles must be positive and queue_reduction must be in [0, 1]")
    rng = random.Random(seed)
    rows = []
    for cycle_id in range(1, cycles + 1):
        loaded = round(rng.uniform(12, 22), 2)
        queue = round(rng.uniform(2, 14), 2)
        loading = round(rng.uniform(3, 7), 2)
        empty = round(rng.uniform(9, 18), 2)
        dumping = round(rng.uniform(2, 5), 2)
        baseline = round(loaded + queue + loading + empty + dumping, 2)
        reduced_queue = round(queue * (1 - queue_reduction), 2)
        alternative = round(loaded + reduced_queue + loading + empty + dumping, 2)
        rows.append({
            "cycle_id": cycle_id, "loaded_travel_min": loaded, "queue_min": queue,
            "loading_min": loading, "empty_travel_min": empty, "dumping_min": dumping,
            "baseline_cycle_min": baseline, "alternative_queue_min": reduced_queue,
            "alternative_cycle_min": alternative,
        })
    return rows


def summarize(rows: list[dict], queue_reduction: float, seed: int) -> dict:
    if not rows:
        raise ValueError("No cycles to summarize")
    baseline = [row["baseline_cycle_min"] for row in rows]
    alternative = [row["alternative_cycle_min"] for row in rows]
    return {
        "data_kind": "synthetic_simulation", "seed": seed, "cycles": len(rows),
        "queue_reduction_fraction": queue_reduction, "unit": "minutes",
        "baseline_mean": round(statistics.mean(baseline), 2),
        "alternative_mean": round(statistics.mean(alternative), 2),
        "baseline_median": round(statistics.median(baseline), 2),
        "alternative_median": round(statistics.median(alternative), 2),
        "mean_difference": round(statistics.mean(baseline) - statistics.mean(alternative), 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--cycles", type=int, default=120)
    parser.add_argument("--queue-reduction", type=float, default=0.30)
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()
    try:
        rows = simulate(args.seed, args.cycles, args.queue_reduction)
    except ValueError as exc:
        parser.error(str(exc))
    args.output.mkdir(parents=True, exist_ok=True)
    with (args.output / "cycles.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = summarize(rows, args.queue_reduction, args.seed)
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
