# ------------------------
# fix_structure.py
# ------------------------
#!/usr/bin/env python3
"""
Fix script to clean up incorrect directory structure.

Run this from the project root: python fix_structure.py
"""

import os
import shutil
from pathlib import Path

def fix_structure():
    """Remove incorrectly placed directories."""
    
    project_root = Path(__file__).parent
    
    # Directories that should NOT exist at src/ level
    wrong_dirs = [
        project_root / "src" / "extract",
        project_root / "src" / "query",
        project_root / "src" / "io",
        project_root / "src" / "templates",
    ]
    
    removed = []
    for wrong_dir in wrong_dirs:
        if wrong_dir.exists():
            print(f"Removing incorrect directory: {wrong_dir}")
            shutil.rmtree(wrong_dir)
            removed.append(str(wrong_dir))
    
    if removed:
        print(f"\n✓ Removed {len(removed)} incorrect directories")
        print("\nCorrect structure should be:")
        print("  src/")
        print("    json_extractor/")
        print("      extract/")
        print("      io/")
        print("      query/")
        print("      templates/")
    else:
        print("✓ No incorrect directories found - structure is correct!")
    
    # Verify correct structure exists
    required_dirs = [
        project_root / "src" / "json_extractor",
        project_root / "src" / "json_extractor" / "extract",
        project_root / "src" / "json_extractor" / "io",
        project_root / "src" / "json_extractor" / "query",
        project_root / "src" / "json_extractor" / "templates",
    ]
    
    missing = []
    for req_dir in required_dirs:
        if not req_dir.exists():
            missing.append(str(req_dir))
    
    if missing:
        print("\n⚠ Missing required directories:")
        for m in missing:
            print(f"  - {m}")
        print("\nPlease re-extract the project files.")
    else:
        print("\n✓ All required directories present")
    
    # Check for __init__.py files
    init_files = [
        project_root / "src" / "__init__.py",
        project_root / "src" / "json_extractor" / "__init__.py",
        project_root / "src" / "json_extractor" / "extract" / "__init__.py",
        project_root / "src" / "json_extractor" / "io" / "__init__.py",
        project_root / "src" / "json_extractor" / "query" / "__init__.py",
        project_root / "src" / "json_extractor" / "templates" / "__init__.py",
    ]
    
    missing_init = []
    for init_file in init_files:
        if not init_file.exists():
            missing_init.append(str(init_file))
            # Create it
            init_file.parent.mkdir(parents=True, exist_ok=True)
            init_file.write_text('"""\nPackage marker.\n"""\n')
            print(f"✓ Created {init_file}")
    
    if not missing_init:
        print("\n✓ All __init__.py files present")

if __name__ == "__main__":
    fix_structure()
    print("\n" + "="*50)
    print("Fix complete! Now try:")
    print("  streamlit run app.py")
    print("="*50)
