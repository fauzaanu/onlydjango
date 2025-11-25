#!/usr/bin/env python3
"""
Keep steering files synchronized across multiple IDE formats.

Discovers rules from all configured editors and keeps them in sync bidirectionally.

Usage:
    uv run python sync_rules.py
"""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple


WORKSPACE_ROOT = Path(__file__).resolve().parent


@dataclass
class FrontMatterConfig:
    """Configuration for how an editor represents front matter."""
    
    always: Dict[str, str]  # {"key": "value"} for always-apply rules
    glob: Dict[str, str]  # {"key": "value"} for glob-based rules
    manual: Dict[str, str]  # {"key": "value"} for manual-trigger rules
    pattern_key: str  # Key name for the glob pattern
    pattern_format: Optional[str] = None  # Format string for pattern, e.g. "['{pattern}']"
    other_keys: list[str] = None  # Other keys to preserve
    
    def __post_init__(self):
        if self.other_keys is None:
            self.other_keys = []


@dataclass
class EditorConfig:
    """Configuration for an IDE/editor."""
    
    name: str
    rules_dir: Path
    front_matter: FrontMatterConfig
    special_file: Optional[Path] = None  # Where to copy .rules content


class RuleFile:
    """Represents a single rule file with its metadata and content."""
    
    def __init__(self, path: Path, front_matter: Dict[str, str], body: str):
        self.path = path
        self.front_matter = front_matter
        self.body = body
        self.name = path.name
    
    def is_always_apply(self, config: FrontMatterConfig) -> bool:
        """Check if this rule always applies based on editor config."""
        for key, value in config.always.items():
            if self.front_matter.get(key.lower()) == value.lower():
                return True
        return False
    
    def is_glob_based(self, config: FrontMatterConfig) -> bool:
        """Check if this rule is glob-based."""
        for key, value in config.glob.items():
            if self.front_matter.get(key.lower()) == value.lower():
                return True
        return False
    
    def is_manual(self, config: FrontMatterConfig) -> bool:
        """Check if this rule is manually triggered."""
        for key, value in config.manual.items():
            if self.front_matter.get(key.lower()) == value.lower():
                return True
        return False
    
    def get_pattern(self, config: FrontMatterConfig) -> Optional[str]:
        """Extract the glob pattern."""
        pattern = self.front_matter.get(config.pattern_key.lower())
        if not pattern:
            return None
        # Strip formatting like ['...'] or quotes
        return pattern.strip("[]'\"")


class EditorSync:
    """Handles synchronization between multiple editors."""
    
    def __init__(self, editors: list[EditorConfig], rules_file: Path):
        self.editors = editors
        self.rules_file = rules_file
    
    def parse_front_matter(self, text: str) -> Tuple[Dict[str, str], str]:
        """Parse front matter and return (metadata, content)."""
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
        
        content_lines = lines[end + 1:]
        content = "\n".join(content_lines).lstrip("\n")
        return res, content
    
    def build_front_matter(self, metadata: Dict[str, str]) -> str:
        """Build front matter block from metadata dict."""
        if not metadata:
            return ""
        
        lines = ["---"]
        for k, v in metadata.items():
            lines.append(f"{k}: {v}")
        lines.append("---")
        return "\n".join(lines)
    
    def discover_rules(self) -> Dict[str, RuleFile]:
        """Discover all unique rules from all editors."""
        all_rules: Dict[str, RuleFile] = {}
        
        for editor in self.editors:
            if not editor.rules_dir.exists():
                continue
            
            for rule_path in sorted(editor.rules_dir.glob("*.md")):
                if rule_path.name in ["agents.md", "claude.md"]:
                    continue
                
                content = rule_path.read_text(encoding="utf-8")
                fm, body = self.parse_front_matter(content)
                
                # Use filename as key - assume same filename = same rule
                if rule_path.name not in all_rules:
                    all_rules[rule_path.name] = RuleFile(rule_path, fm, body)
        
        return all_rules
    
    def convert_front_matter(
        self, rule: RuleFile, source_config: FrontMatterConfig, target_config: FrontMatterConfig
    ) -> Dict[str, str]:
        """Convert front matter from source format to target format."""
        result = {}
        
        if rule.is_always_apply(source_config):
            result.update(target_config.always)
        elif rule.is_manual(source_config):
            result.update(target_config.manual)
        elif rule.is_glob_based(source_config):
            result.update(target_config.glob)
            pattern = rule.get_pattern(source_config)
            if pattern:
                if target_config.pattern_format:
                    result[target_config.pattern_key] = target_config.pattern_format.format(
                        pattern=pattern
                    )
                else:
                    result[target_config.pattern_key] = pattern
        
        return result
    
    def sync(self) -> int:
        """Sync all rules across all editors."""
        print("Discovering rules from all editors...\n")
        
        # Discover all unique rules
        all_rules = self.discover_rules()
        
        if not all_rules:
            print("No rules found to sync")
            return 1
        
        print(f"Found {len(all_rules)} unique rules\n")
        print("Syncing across all editors...\n")
        
        # For each editor, ensure it has all rules in its format
        for editor in self.editors:
            editor.rules_dir.mkdir(parents=True, exist_ok=True)
            
            # Clear existing rules (except special files)
            for f in editor.rules_dir.glob("*.md"):
                if f.name not in ["agents.md", "claude.md"]:
                    f.unlink()
            
            # Write all rules in this editor's format
            for rule_name, rule in sorted(all_rules.items()):
                # Detect source format by checking which config matches
                source_config = None
                for src_editor in self.editors:
                    if (
                        rule.is_always_apply(src_editor.front_matter)
                        or rule.is_manual(src_editor.front_matter)
                        or rule.is_glob_based(src_editor.front_matter)
                    ):
                        source_config = src_editor.front_matter
                        break
                
                if not source_config:
                    # Default to first editor's format
                    source_config = self.editors[0].front_matter
                
                # Convert to target format
                target_fm = self.convert_front_matter(rule, source_config, editor.front_matter)
                target_content = self.build_front_matter(target_fm) + "\n\n" + rule.body
                
                target_file = editor.rules_dir / rule_name
                target_file.write_text(target_content, encoding="utf-8")
            
            print(f"✓ {editor.name}: {len(all_rules)} rules")
        
        # Sync .rules file to special files
        if self.rules_file.exists():
            rules_content = self.rules_file.read_text(encoding="utf-8")
            print()
            for editor in self.editors:
                if editor.special_file:
                    editor.special_file.write_text(rules_content, encoding="utf-8")
                    print(f"✓ .rules → {editor.special_file.name} ({editor.name})")
        
        print(f"\n✓ All editors synchronized")
        return 0


# Editor configurations
EDITORS = [
    EditorConfig(
        name="kiro",
        rules_dir=WORKSPACE_ROOT / ".kiro" / "steering",
        front_matter=FrontMatterConfig(
            always={"inclusion": "always"},
            manual={"inclusion": "manual"},
            glob={"inclusion": "filematch"},
            pattern_key="fileMatchPattern",
            pattern_format="'{pattern}'",
        ),
    ),
    EditorConfig(
        name="antigravity",
        rules_dir=WORKSPACE_ROOT / ".agent" / "rules",
        special_file=WORKSPACE_ROOT /  "GEMINI.md",
        front_matter=FrontMatterConfig(
            always={"trigger": "always_on"},
            manual={"trigger": "manual"},
            glob={"trigger": "glob"},
            pattern_key="globs",
        ),
    ),
    EditorConfig(
        name="cursor",
        rules_dir=WORKSPACE_ROOT / ".cursor" / "rules",
        special_file=WORKSPACE_ROOT /  "AGENTS.md",
        front_matter=FrontMatterConfig(
            always={"alwaysApply": "true"},  # Always Apply
            manual={"alwaysApply": "false"},  # Apply Manually (false + no glob)
            glob={"alwaysApply": "false"},  # Apply to Specific Files (false + glob)
            pattern_key="globs",
            pattern_format="['{pattern}']",
        ),
    ),
]

RULES_FILE = WORKSPACE_ROOT / ".rules"


def main(argv=None):
    argv = argv if argv is not None else sys.argv
    
    parser = argparse.ArgumentParser(
        description="Keep steering files synchronized across multiple IDE formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Discovers rules from all editors and keeps them in sync bidirectionally.",
    )
    
    args = parser.parse_args(argv[1:])
    
    syncer = EditorSync(EDITORS, RULES_FILE)
    return syncer.sync()


if __name__ == "__main__":
    raise SystemExit(main())
