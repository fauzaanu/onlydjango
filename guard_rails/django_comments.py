"""
Convert HTML comments to Django comments in all .html files.
HTML comments are visible in client-side source, Django comments are not.
"""
import re
from pathlib import Path


def convert_comments(content):
    """Convert HTML comments to Django comments."""
    # Replace <!-- comment --> with {% comment %}comment{% endcomment %}
    # This handles both single-line and multi-line comments
    pattern = r'<!--(.*?)-->'
    replacement = r'{% comment %}\1{% endcomment %}'
    
    converted = re.sub(pattern, replacement, content, flags=re.DOTALL)
    return converted


def check_git_status():
    """Check if there are uncommitted changes in tracked files."""
    import subprocess
    
    try:
        # Check if we're in a git repo
        result = subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            print("Warning: Not in a git repository. Proceeding anyway.")
            return True
        
        # Check for uncommitted changes in tracked files
        result = subprocess.run(
            ['git', 'diff', '--name-only'],
            capture_output=True,
            text=True,
            check=False
        )
        
        uncommitted = result.stdout.strip()
        
        if uncommitted:
            print("ERROR: You have uncommitted changes in tracked files:")
            print(uncommitted)
            print("\nPlease commit all changes before running this script.")
            print("Run: git add . && git commit -m 'your message'")
            return False
        
        # Also check staged but uncommitted
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True,
            text=True,
            check=False
        )
        
        staged = result.stdout.strip()
        
        if staged:
            print("ERROR: You have staged but uncommitted changes:")
            print(staged)
            print("\nPlease commit all changes before running this script.")
            print("Run: git commit -m 'your message'")
            return False
        
        return True
        
    except FileNotFoundError:
        print("Warning: git not found. Proceeding anyway.")
        return True


def main():
    """Find and convert all HTML comments to Django comments."""
    # Check git status first
    if not check_git_status():
        return
    
    root_dir = Path('.')
    html_files = list(root_dir.rglob('*.html'))
    
    if not html_files:
        print("No .html files found.")
        return
    
    print(f"Found {len(html_files)} HTML files")
    print("\nProcessing files...\n")
    
    converted_count = 0
    
    for html_file in sorted(html_files):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                original = f.read()
            
            # Check if file has HTML comments
            if '<!--' not in original:
                continue
            
            # Convert comments
            converted = convert_comments(original)
            
            # Write back
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(converted)
            
            # Count how many comments were converted
            comment_count = original.count('<!--')
            converted_count += 1
            
            print(f"✓ {html_file} ({comment_count} comments converted)")
            
        except Exception as e:
            print(f"✗ Error processing {html_file}: {e}")
    
    print(f"\n{'='*80}")
    print(f"Converted {converted_count} files")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()
