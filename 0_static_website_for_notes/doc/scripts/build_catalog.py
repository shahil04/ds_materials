"""Generate the static website catalog from repository files."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Iterable


IGNORED_DIRECTORIES = {".git", ".github", "__pycache__", "_site", "node_modules", ".venv", "venv"}
IGNORED_FILENAMES = {"catalog.json"}


def natural_sort_key(value: str) -> tuple[tuple[int, object], ...]:
    """Sort digit runs numerically so Module 2 comes before Module 10."""
    parts: list[tuple[int, object]] = []
    for part in re.split(r"(\d+)", value.casefold()):
        if part.isdigit():
            parts.append((0, int(part)))
        else:
            parts.append((1, part))
    return tuple(parts)


def catalog_files(root: Path) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for current, directories, filenames in os.walk(root):
        directories[:] = sorted(
            directory
            for directory in directories
            if directory not in IGNORED_DIRECTORIES and not directory.startswith(".")
        )
        for filename in filenames:
            path = Path(current, filename)
            if (
                path.name.startswith("~$")
                or path.name.startswith(".")
                or path.name.casefold() in IGNORED_FILENAMES
            ):
                continue

            relative_path = path.relative_to(root).as_posix()
            parent = Path(relative_path).parent.as_posix()
            extension = path.suffix.casefold()
            items.append(
                {
                    "path": relative_path,
                    "name": path.name,
                    "folder": "" if parent == "." else parent,
                    "extension": extension or "file",
                }
            )

    return sorted(items, key=lambda item: natural_sort_key(item["path"]))


def write_catalog(root: Path, output: Path) -> int:
    items = catalog_files(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(items)


def parse_args(arguments: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, help="Catalog path (defaults to <root>/catalog.json)")
    return parser.parse_args(arguments)


def main() -> None:
    args = parse_args()
    root = args.root.resolve()
    output = args.output or Path(__file__).resolve().parents[1] / "catalog.json"
    if not output.is_absolute():
        output = root / output
    count = write_catalog(root, output)
    print(f"Wrote {count} files to {output}")


if __name__ == "__main__":
    main()
