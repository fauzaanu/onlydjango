#!/usr/bin/env python3
"""
Steering file selector - replicates Kiro's steering mechanism for other IDEs.

Kiro IDE has built-in steering file support. This script brings the same behavior
to IDEs that don't support steering natively (Cursor, Windsurf, etc.).

Usage:
    uv run python get_steering.py              # Show all 'always' inclusion files
    uv run python get_steering.py --default    # Same as above (explicit)
    uv run python get_steering.py <path>       # Show 'fileMatch' files matching path
"""

from __future__ import annotations

import argparse
import fnmatch
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

WORKSPACE_ROOT = Path(__file__).resolve().parent
STEERING_DIR = WORKSPACE_ROOT / ".kiro" / "steering"
WORKSPACE_AGENTS = WORKSPACE_ROOT / "AGENTS.md"


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def parse_front_matter(text: str) -> Dict[str, str]:
    res: Dict[str, str] = {}
    if not text.lstrip().startswith("---"):
        return res
    lines = text.splitlines()
    end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
    if end is None:
        return res
    for line in lines[1:end]:
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        res[k.strip().lower()] = v.strip().strip("'\"")
    return res


def collect_steering_files() -> List[Path]:
    files: List[Path] = []
    if STEERING_DIR.is_dir():
        files.extend(sorted(STEERING_DIR.rglob("*.md")))
    if WORKSPACE_AGENTS.is_file():
        files.insert(0, WORKSPACE_AGENTS)
    return files


def normalize_target_posix(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    p = Path(raw)
    try:
        if p.is_absolute():
            p = p.relative_to(WORKSPACE_ROOT)
    except ValueError:
        pass
    return p.as_posix()


def matches_pattern(pattern: str, target_posix: str) -> bool:
    if fnmatch.fnmatch(target_posix, pattern):
        return True
    target = Path(target_posix)
    if fnmatch.fnmatch(target.name, pattern):
        return True
    if pattern.startswith("**/"):
        stripped = pattern[3:]
        if fnmatch.fnmatch(target_posix, stripped) or fnmatch.fnmatch(target.name, stripped):
            return True
    return False


def find_matches(target: Optional[str], default_mode: bool) -> List[Tuple[Path, str]]:
    out: List[Tuple[Path, str]] = []
    files = collect_steering_files()
    target_posix = normalize_target_posix(target)

    for p in files:
        content = read_text(p)
        fm = parse_front_matter(content)
        inclusion = fm.get("inclusion", "always").strip().lower()
        pattern = fm.get("filematchpattern")

        if default_mode or target_posix is None:
            if inclusion == "always":
                out.append((p, content))
        elif inclusion == "filematch" and pattern:
            if matches_pattern(pattern.strip(), target_posix):
                out.append((p, content))

    return out


def print_results(matches: List[Tuple[Path, str]]) -> None:
    if not matches:
        print("No steering files need to be included.")
        return

    print("Included steering files:")
    for p, _ in matches:
        try:
            rel = p.relative_to(WORKSPACE_ROOT)
        except ValueError:
            rel = p
        print(f" - {rel}")
    print("\n---\n")

    for p, content in matches:
        try:
            rel = p.relative_to(WORKSPACE_ROOT)
        except ValueError:
            rel = p
        print(f"### BEGIN: {rel}\n")
        print(content.rstrip())
        print(f"\n### END: {rel}\n")


def main(argv: Optional[List[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv

    parser = argparse.ArgumentParser(
        description="Select steering files based on inclusion rules.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run python get_steering.py              # All 'always' files
  uv run python get_steering.py --default    # Same as above
  uv run python get_steering.py src/app.py   # Files matching src/app.py
  uv run python get_steering.py file.html    # Files matching file.html
""",
    )
    parser.add_argument(
        "--default",
        action="store_true",
        help="Show all 'always' inclusion steering files (same as no arguments)",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="File path to match against fileMatch patterns",
    )

    args = parser.parse_args(argv[1:])

    if args.default and args.path:
        parser.error("Cannot use --default with a path argument")

    matches = find_matches(args.path, args.default)
    print_results(matches)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
