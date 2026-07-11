# ------------------------
# check_files.py
# ------------------------
#!/usr/bin/env python3
"""
Complete file verification and download helper.

This script will:
1. Check which files are missing or corrupted
2. Provide download links for each missing file
3. Show exactly where each file should be placed
"""

import sys
from pathlib import Path
import hashlib

def get_file_hash(filepath):
    """Get MD5 hash of a file."""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def check_file_content(filepath, min_lines=10):
    """Check if file has minimum content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return len(lines) >= min_lines
    except:
        return False

def main():
    print("JSON Extractor vNext - Complete File Check")
    print("=" * 70)
    
    project_root = Path(__file__).parent
    
    # Define all required files with their expected minimum sizes
    required_files = {
        "Root files": [
            ("app.py", 200, "Streamlit GUI application"),
            ("cli.py", 150, "Command-line interface"),
            ("requirements.txt", 5, "Python dependencies"),
            ("README.md", 100, "Documentation"),
            ("QUICKSTART.md", 50, "Quick start guide"),
            ("PROJECT_INFO.md", 100, "Project information"),
        ],
        "Data files": [
            ("DATA/example_document.json", 50, "Example DOCUMENT records"),
            ("DATA/example_regulation.json", 50, "Example RULE records"),
        ],
        "Core package": [
            ("src/__init__.py", 1, "Package marker"),
            ("src/json_extractor/__init__.py", 5, "Main package init"),
            ("src/json_extractor/config.py", 180, "Configuration and preferences"),
            ("src/json_extractor/pipeline.py", 150, "Main pipeline orchestration"),
        ],
        "IO module": [
            ("src/json_extractor/io/__init__.py", 5, "IO package init"),
            ("src/json_extractor/io/files.py", 80, "File discovery and reading"),
            ("src/json_extractor/io/export.py", 100, "CSV/XLSX export"),
        ],
        "Extract module": [
            ("src/json_extractor/extract/__init__.py", 5, "Extract package init"),
            ("src/json_extractor/extract/load_and_flatten.py", 400, "JSON normalization and validation"),
        ],
        "Query module": [
            ("src/json_extractor/query/__init__.py", 5, "Query package init"),
            ("src/json_extractor/query/schema.py", 100, "Query field definitions"),
            ("src/json_extractor/query/compiler.py", 200, "DSL parser"),
            ("src/json_extractor/query/engine.py", 100, "Query execution"),
        ],
        "Templates module": [
            ("src/json_extractor/templates/__init__.py", 3, "Templates package init"),
            ("src/json_extractor/templates/app_b.py", 60, "Appendix B template"),
        ],
    }
    
    missing = []
    corrupted = []
    ok = []
    
    for category, files in required_files.items():
        print(f"\n{category}:")
        for rel_path, min_lines, description in files:
            filepath = project_root / rel_path
            
            if not filepath.exists():
                print(f"  ✗ MISSING: {rel_path}")
                print(f"     → {description}")
                missing.append((rel_path, description))
            elif not check_file_content(filepath, min_lines):
                print(f"  ⚠ CORRUPTED/INCOMPLETE: {rel_path}")
                print(f"     → Expected at least {min_lines} lines, file may be truncated")
                print(f"     → {description}")
                corrupted.append((rel_path, description))
            else:
                print(f"  ✓ {rel_path}")
                ok.append(rel_path)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✓ OK: {len(ok)} files")
    print(f"✗ Missing: {len(missing)} files")
    print(f"⚠ Corrupted/Incomplete: {len(corrupted)} files")
    
    if missing or corrupted:
        print("\n" + "=" * 70)
        print("ACTION REQUIRED")
        print("=" * 70)
        
        if missing:
            print(f"\n📥 MISSING FILES ({len(missing)}):")
            print("\nYou need to download these files from the original package:")
            for rel_path, description in missing:
                print(f"\n  File: {rel_path}")
                print(f"  Description: {description}")
                print(f"  Place at: {project_root / rel_path}")
        
        if corrupted:
            print(f"\n⚠️  CORRUPTED/INCOMPLETE FILES ({len(corrupted)}):")
            print("\nThese files exist but appear incomplete or corrupted.")
            print("Please re-download and replace them:")
            for rel_path, description in corrupted:
                print(f"\n  File: {rel_path}")
                print(f"  Description: {description}")
                print(f"  Location: {project_root / rel_path}")
        
        print("\n" + "=" * 70)
        print("HOW TO FIX:")
        print("=" * 70)
        print("""
1. Go back to Claude and ask for the complete file package
2. Download ALL files from the outputs folder
3. Extract to your project directory: F:\\xPy\\Json\\
4. Run this script again to verify: python check_files.py
5. Once all files pass, run: streamlit run app.py
        """)
        
        return 1
    else:
        print("\n" + "🎉" * 35)
        print("\n✨ ALL FILES VERIFIED!")
        print("\n🚀 You can now run the application:")
        print("   streamlit run app.py")
        print("   python cli.py --help")
        print("\n" + "🎉" * 35)
        return 0

if __name__ == "__main__":
    sys.exit(main())