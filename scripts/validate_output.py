#!/usr/bin/env python3
"""Validate a model -> videos -> comments JSON deliverable."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


DATE_FORMATS = (
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
    "%Y/%m/%d %H:%M:%S",
    "%Y/%m/%d",
)


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def load_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise SystemExit("ERROR: top-level JSON must be a list")
    return data


def validate(data: list[dict[str, Any]], start: datetime | None, end: datetime | None) -> tuple[Counter, list[str]]:
    stats: Counter = Counter()
    issues: list[str] = []
    seen_comments: set[str] = set()

    for model_index, model_item in enumerate(data):
        model_name = model_item.get("model") or f"model[{model_index}]"
        videos = model_item.get("videos")
        stats["models"] += 1
        if not isinstance(videos, list):
            issues.append(f"{model_name}: videos must be a list")
            continue
        if videos:
            stats["nonzero_models"] += 1
        else:
            stats["zero_models"] += 1

        for video_index, video in enumerate(videos):
            stats["videos"] += 1
            video_id = video.get("videoId") or f"{model_name}/video[{video_index}]"
            if not video.get("videoUrl"):
                stats["missing_video_url"] += 1
                issues.append(f"{model_name}/{video_id}: missing videoUrl")
            comments = video.get("comments")
            if not isinstance(comments, list):
                issues.append(f"{model_name}/{video_id}: comments must be a list")
                continue

            previous_time: datetime | None = None
            for comment_index, comment in enumerate(comments):
                stats["comments"] += 1
                comment_id = str(comment.get("commentId") or "").strip()
                content = str(comment.get("content") or "").strip()
                created_at = parse_time(comment.get("createTime"))

                if not comment_id:
                    stats["missing_comment_id"] += 1
                    comment_id = f"missing:{model_name}:{video_id}:{comment_index}:{content}:{comment.get('createTime')}"
                if not content:
                    stats["missing_content"] += 1
                    issues.append(f"{model_name}/{video_id}/{comment_id}: missing content")
                if not created_at:
                    stats["missing_or_invalid_comment_time"] += 1
                    issues.append(f"{model_name}/{video_id}/{comment_id}: missing or invalid createTime")
                else:
                    if start and created_at < start:
                        stats["out_of_range_time"] += 1
                        issues.append(f"{model_name}/{video_id}/{comment_id}: createTime before start")
                    if end and created_at > end:
                        stats["out_of_range_time"] += 1
                        issues.append(f"{model_name}/{video_id}/{comment_id}: createTime after end")
                    if previous_time and created_at > previous_time:
                        stats["ascending_time_pairs"] += 1
                    previous_time = created_at

                duplicate_key = f"{model_name}|{video_id}|{comment_id}"
                if duplicate_key in seen_comments:
                    stats["duplicate_comments"] += 1
                    issues.append(f"{model_name}/{video_id}/{comment_id}: duplicate comment")
                seen_comments.add(duplicate_key)

    return stats, issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a comment collection JSON deliverable.")
    parser.add_argument("json_path", type=Path)
    parser.add_argument("--start", help="inclusive start date, e.g. 2026-04-01")
    parser.add_argument("--end", help="inclusive end date, e.g. 2026-05-08 23:59:59")
    parser.add_argument("--max-issues", type=int, default=30)
    args = parser.parse_args()

    start = parse_time(args.start) if args.start else None
    end = parse_time(args.end) if args.end else None
    data = load_json(args.json_path)
    stats, issues = validate(data, start, end)

    print("Validation summary")
    for key in (
        "models",
        "nonzero_models",
        "zero_models",
        "videos",
        "comments",
        "duplicate_comments",
        "missing_video_url",
        "missing_comment_id",
        "missing_content",
        "missing_or_invalid_comment_time",
        "out_of_range_time",
        "ascending_time_pairs",
    ):
        print(f"- {key}: {stats[key]}")

    if issues:
        print("\nIssues")
        for issue in issues[: args.max_issues]:
            print(f"- {issue}")
        if len(issues) > args.max_issues:
            print(f"- ... {len(issues) - args.max_issues} more")
        raise SystemExit(1)

    print("\nOK: no blocking issues found")


if __name__ == "__main__":
    main()

