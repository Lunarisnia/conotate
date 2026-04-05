#!/usr/bin/env python3
import sys


def fetch_domain(slug, file_path):
    start_marker = f"<!-- domain: {slug} -->"
    end_marker = f"<!-- end:{slug} -->"

    try:
        with open(file_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: file not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    start = content.find(start_marker)
    if start == -1:
        print(
            f"Error: domain block '{start_marker}' not found in {file_path}",
            file=sys.stderr,
        )
        sys.exit(1)

    end = content.find(end_marker, start)
    if end == -1:
        print(
            f"Error: closing marker '{end_marker}' not found in {file_path}",
            file=sys.stderr,
        )
        sys.exit(1)

    end += len(end_marker)
    print(content[start:end])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: fetch_domain.py <slug> <file_path>", file=sys.stderr)
        sys.exit(1)
    fetch_domain(sys.argv[1], sys.argv[2])
