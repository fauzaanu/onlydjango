#!/usr/bin/env python3
"""
Usage:
    uv run python get_steering.py <path>
    uv run python get_steering.py <path> --include-defaults
"""

from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

WORKSPACE_ROOT = Path(__file__).resolve().parent
STEERING_DIR = WORKSPACE_ROOT / ".kiro" / "steering"


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def parse_front_matter(text: str) -> Tuple[Dict[str, str], str]:
    """Parse front matter and return (metadata, content_without_frontmatter)."""
    res: Dict[str, str] = {}
    if not text.lstrip().startswith("---"):
        return res, text
    lines = text.splitlines()
    end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
    if end is None:
        return res, text
    for line in lines[1:end]:
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        res[k.strip().lower()] = v.strip().strip("'\"")
    # Return content after frontmatter
    content_lines = lines[end + 1 :]
    content = "\n".join(content_lines).lstrip("\n")
    return res, content


def collect_steering_files() -> List[Path]:
    files: List[Path] = []
    if STEERING_DIR.is_dir():
        files.extend(sorted(STEERING_DIR.glob("*.md")))
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


def find_matches(
    target: Optional[str], include_defaults: bool
) -> List[Tuple[Path, str, Dict[str, str]]]:
    """Find matching steering files.
    
    Returns list of (path, content_without_frontmatter, frontmatter_dict).
    """
    out: List[Tuple[Path, str, Dict[str, str]]] = []
    files = collect_steering_files()
    target_posix = normalize_target_posix(target)
    seen_paths: set[Path] = set()

    # If include_defaults, first add all 'always' files
    if include_defaults:
        for p in files:
            content = read_text(p)
            fm, clean_content = parse_front_matter(content)
            inclusion = fm.get("inclusion", "always").strip().lower()
            if inclusion == "always":
                out.append((p, clean_content, fm))
                seen_paths.add(p)

    # Then add fileMatch matches for the target path
    if target_posix:
        for p in files:
            if p in seen_paths:
                continue
            content = read_text(p)
            fm, clean_content = parse_front_matter(content)
            inclusion = fm.get("inclusion", "always").strip().lower()
            pattern = fm.get("filematchpattern")

            if inclusion == "filematch" and pattern:
                if matches_pattern(pattern.strip(), target_posix):
                    out.append((p, clean_content, fm))
    elif not include_defaults:
        # No target and no include_defaults - show all 'always' files
        for p in files:
            content = read_text(p)
            fm, clean_content = parse_front_matter(content)
            inclusion = fm.get("inclusion", "always").strip().lower()
            if inclusion == "always":
                out.append((p, clean_content, fm))

    return out


def make_xml_tag_name(path: Path) -> str:
    """Convert path to valid XML tag name."""
    try:
        rel = path.relative_to(WORKSPACE_ROOT)
    except ValueError:
        rel = path
    # Use just the filename for cleaner tags
    name = rel.name
    # Replace invalid XML chars with underscores
    name = re.sub(r"[^a-zA-Z0-9_.-]", "_", name)
    return name


def print_results(matches: List[Tuple[Path, str, Dict[str, str]]]) -> None:
    if not matches:
        print("No steering files need to be included.")
        return

    for p, content, _ in matches:
        tag = make_xml_tag_name(p)
        # Indent content for YAML block scalar
        indented = "\n".join("  " + line if line else "" for line in content.rstrip().splitlines())
        print(f"{tag}: |")
        print(indented)
        print()


def main(argv: Optional[List[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv

    parser = argparse.ArgumentParser(
        description="Select steering files based on inclusion rules.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run python get_steering.py                          # All 'always' files
  uv run python get_steering.py src/app.py               # Files matching src/app.py only
  uv run python get_steering.py src/app.py --include-defaults  # 'always' + matching files
""",
    )
    parser.add_argument(
        "--include-defaults",
        action="store_true",
        help="Include all 'always' inclusion steering files along with path matches",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="File path to match against fileMatch patterns",
    )

    args = parser.parse_args(argv[1:])

    matches = find_matches(args.path, args.include_defaults)
    print_results(matches)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
