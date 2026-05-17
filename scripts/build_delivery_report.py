#!/usr/bin/env python3
"""Build a Markdown delivery report from a comment JSON file."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def load_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise SystemExit("ERROR: top-level JSON must be a list")
    return data


def count_model(item: dict[str, Any]) -> dict[str, Any]:
    videos = item.get("videos") or []
    comment_count = 0
    missing_url = 0
    missing_time = 0
    duplicate_keys: set[str] = set()
    duplicate_count = 0

    for video in videos:
        if not video.get("videoUrl"):
            missing_url += 1
        video_id = video.get("videoId") or ""
        for comment in video.get("comments") or []:
            comment_count += 1
            if not comment.get("createTime"):
                missing_time += 1
            key = f"{video_id}|{comment.get('commentId') or comment.get('content')}"
            if key in duplicate_keys:
                duplicate_count += 1
            duplicate_keys.add(key)

    return {
        "model": item.get("model", ""),
        "videos": len(videos),
        "comments": comment_count,
        "missing_url": missing_url,
        "missing_time": missing_time,
        "duplicates": duplicate_count,
    }


def build_report(data: list[dict[str, Any]], low_threshold: int) -> str:
    rows = [count_model(item) for item in data]
    totals = Counter()
    for row in rows:
        totals["models"] += 1
        totals["videos"] += row["videos"]
        totals["comments"] += row["comments"]
        totals["missing_url"] += row["missing_url"]
        totals["missing_time"] += row["missing_time"]
        totals["duplicates"] += row["duplicates"]
        if row["comments"] > 0:
            totals["nonzero_models"] += 1
        else:
            totals["zero_models"] += 1

    low_rows = [row for row in rows if row["comments"] < low_threshold]
    lines: list[str] = [
        "# Delivery Report",
        "",
        "## Summary",
        "",
        f"- Models: {totals['models']}",
        f"- Non-zero models: {totals['nonzero_models']}",
        f"- Zero models: {totals['zero_models']}",
        f"- Videos: {totals['videos']}",
        f"- Comments: {totals['comments']}",
        f"- Missing video URLs: {totals['missing_url']}",
        f"- Missing comment times: {totals['missing_time']}",
        f"- Duplicate comments: {totals['duplicates']}",
        "",
        "## Model Breakdown",
        "",
        "| Model | Videos | Comments | Missing URLs | Missing Times | Duplicates |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    for row in sorted(rows, key=lambda x: (-x["comments"], x["model"])):
        lines.append(
            f"| {row['model']} | {row['videos']} | {row['comments']} | "
            f"{row['missing_url']} | {row['missing_time']} | {row['duplicates']} |"
        )

    lines.extend(
        [
            "",
            f"## Low Volume Models (< {low_threshold} comments)",
            "",
        ]
    )
    if low_rows:
        lines.extend(["| Model | Videos | Comments | Suggested Note |", "|---|---:|---:|---|"])
        for row in sorted(low_rows, key=lambda x: (x["comments"], x["model"])):
            note = "Needs manual explanation: low public volume, narrow date range, or alias mismatch."
            lines.append(f"| {row['model']} | {row['videos']} | {row['comments']} | {note} |")
    else:
        lines.append("No low-volume models under the configured threshold.")

    lines.extend(
        [
            "",
            "## Delivery Notes",
            "",
            "- Keep raw customer files out of the public repository.",
            "- Explain low-volume targets instead of padding them with irrelevant comments.",
            "- Include source URLs so reviewers can sample-check relevance.",
            "- Re-run validation before packaging final files.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Markdown delivery report.")
    parser.add_argument("json_path", type=Path)
    parser.add_argument("--output", type=Path, default=Path("delivery_report.md"))
    parser.add_argument("--low-threshold", type=int, default=100)
    args = parser.parse_args()

    data = load_json(args.json_path)
    report = build_report(data, args.low_threshold)
    args.output.write_text(report, encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

