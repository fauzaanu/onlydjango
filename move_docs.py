"""
Maybe the LLM shouldnt be discouraged from creating random .md files
---
The problem is polluting the repo but summaries also allows to see what the LLM was thinking when they implemented a change.
If an LLM goes against the requirements, these docs will definitely reveal the reasoning. So instead of scanning the entire repo's code
later on perhaps we can just read the docs and find the inconsistencies much easily.
"""
import os
from pathlib import Path
import shutil
from datetime import datetime

def organize_existing_docs():
    """Organize existing files in .kiro/docs/ into date-based subfolders."""
    root_dir = Path(__file__).parent
    docs_dir = root_dir / '.kiro' / 'docs'
    
    if not docs_dir.exists():
        return 0
    
    # Find all .md files directly in docs directory
    md_files = [f for f in docs_dir.glob('*.md') if f.is_file()]
    
    organized_count = 0
    
    for md_file in md_files:
        try:
            # Get file creation time
            creation_time = os.path.getctime(md_file)
            dt = datetime.fromtimestamp(creation_time)
            
            # Create subfolder name: YYYY-MM-DD_HH-MM
            folder_name = dt.strftime('%Y-%m-%d_%H-%M')
            subfolder = docs_dir / folder_name
            subfolder.mkdir(exist_ok=True)
            
            # Move file to subfolder
            target_path = subfolder / md_file.name
            shutil.move(str(md_file), str(target_path))
            print(f"✓ Organized: {md_file.name} → {folder_name}/")
            organized_count += 1
            
        except Exception as e:
            print(f"✗ Error organizing {md_file.name}: {e}")
    
    return organized_count

def move_markdown_files():
    # Get the root directory (where this script is located)
    root_dir = Path(__file__).parent
    
    # Target directory
    target_dir = root_dir / '.kiro' / 'docs'
    
    # Create target directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all .md files in root directory (not subdirectories)
    # Exclude files already in .kiro directory
    md_files = [f for f in root_dir.glob('*.md') if f.is_file() and '.kiro' not in f.parts]
    
    moved_count = 0
    skipped_files = []
    
    for md_file in md_files:
        # Skip README.md
        if md_file.name.upper() == 'README.MD':
            skipped_files.append(md_file.name)
            continue
        
        try:
            # Get file creation time
            creation_time = os.path.getctime(md_file)
            dt = datetime.fromtimestamp(creation_time)
            
            # Create subfolder name: YYYY-MM-DD_HH-MM
            folder_name = dt.strftime('%Y-%m-%d_%H-%M')
            subfolder = target_dir / folder_name
            subfolder.mkdir(exist_ok=True)
            
            # Target path in subfolder
            target_path = subfolder / md_file.name
            
            # Move the file
            shutil.move(str(md_file), str(target_path))
            print(f"✓ Moved: {md_file.name} → {folder_name}/")
            moved_count += 1
            
        except Exception as e:
            print(f"✗ Error moving {md_file.name}: {e}")
    
    # Organize existing files in .kiro/docs/
    print(f"\n{'='*50}")
    print("Organizing existing files in .kiro/docs/...")
    print(f"{'='*50}")
    organized_count = organize_existing_docs()
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Moved from root: {moved_count} files")
    print(f"  Organized in docs: {organized_count} files")
    print(f"  Skipped: {len(skipped_files)} files")
    if skipped_files:
        print(f"  Skipped files: {', '.join(skipped_files)}")
    print(f"{'='*50}")

if __name__ == '__main__':
    move_markdown_files()
