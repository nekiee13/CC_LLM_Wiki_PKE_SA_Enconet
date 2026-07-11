# ------------------------
# fix_files.py
# ------------------------
#!/usr/bin/env python3
"""
Automated fix script for JSON Extractor vNext file structure.

This will move files to their correct locations.
Run from project root: python fix_files.py
"""

import shutil
from pathlib import Path

def fix_file_structure():
    """Move files to correct locations."""
    
    project_root = Path(__file__).parent
    src_root = project_root / "src" / "json_extractor"
    
    print("JSON Extractor vNext - File Structure Fix")
    print("=" * 60)
    
    # Define where files should be moved
    moves = [
        # (current_location, target_location, description)
        (
            src_root / "compiler.py",
            src_root / "query" / "compiler.py",
            "Move compiler.py to query/"
        ),
        (
            src_root / "load_and_flatten.py",
            src_root / "extract" / "load_and_flatten.py",
            "Move load_and_flatten.py to extract/"
        ),
    ]
    
    moved_count = 0
    for source, target, description in moves:
        if source.exists():
            print(f"\n✓ {description}")
            print(f"  From: {source.relative_to(project_root)}")
            print(f"  To:   {target.relative_to(project_root)}")
            
            # Ensure target directory exists
            target.parent.mkdir(parents=True, exist_ok=True)
            
            # Move the file
            shutil.move(str(source), str(target))
            moved_count += 1
        else:
            # Check if already in correct location
            if target.exists():
                print(f"✓ {description} - Already in correct location")
            else:
                print(f"⚠ {description} - Source file not found!")
    
    print(f"\n{'=' * 60}")
    print(f"Moved {moved_count} file(s)")
    
    # Now check for missing files that need to be created
    print(f"\n{'=' * 60}")
    print("Checking for missing module files...")
    print("=" * 60)
    
    missing_files = []
    
    # Check io/ directory
    io_dir = src_root / "io"
    if not (io_dir / "files.py").exists():
        missing_files.append("src/json_extractor/io/files.py")
    if not (io_dir / "export.py").exists():
        missing_files.append("src/json_extractor/io/export.py")
    
    # Check templates/ directory
    templates_dir = src_root / "templates"
    if not (templates_dir / "app_b.py").exists():
        missing_files.append("src/json_extractor/templates/app_b.py")
    
    if missing_files:
        print("\n⚠️  Missing critical files:")
        for mf in missing_files:
            print(f"  - {mf}")
        print("\n💡 These files need to be extracted from the original package.")
        print("   Please re-download and extract all files from the outputs folder.")
    else:
        print("\n✅ All required files present!")
    
    print(f"\n{'=' * 60}")
    print("NEXT STEPS:")
    print("=" * 60)
    
    if missing_files:
        print("\n1. Re-extract these missing files from the outputs folder:")
        for mf in missing_files:
            print(f"   - {mf}")
        print("\n2. Then run: python verify_install.py")
    else:
        print("\n1. Run verification: python verify_install.py")
        print("2. If all checks pass: streamlit run app.py")
    
    print()

if __name__ == "__main__":
    fix_file_structure()
