# ------------------------
# verify_install.py
# ------------------------
#!/usr/bin/env python3
"""
Verify installation script.

Run this from the project root: python verify_install.py
"""

import sys
from pathlib import Path

def verify_installation():
    """Verify the installation is correct."""
    
    print("JSON Extractor vNext - Installation Verification")
    print("=" * 60)
    
    project_root = Path(__file__).parent
    errors = []
    warnings = []
    
    # 1. Check directory structure
    print("\n1. Checking directory structure...")
    required_dirs = {
        "Root files": [
            project_root / "cli.py",
            project_root / "requirements.txt",
            project_root / "README.md",
        ],
        "Data directory": [
            project_root / "DATA",
        ],
        "Source package": [
            project_root / "src",
            project_root / "src" / "json_extractor",
            project_root / "src" / "json_extractor" / "extract",
            project_root / "src" / "json_extractor" / "io",
            project_root / "src" / "json_extractor" / "query",
            project_root / "src" / "json_extractor" / "templates",
        ],
    }
    
    for category, paths in required_dirs.items():
        print(f"\n  {category}:")
        for path in paths:
            if path.exists():
                print(f"    ✓ {path.name}")
            else:
                print(f"    ✗ MISSING: {path.name}")
                errors.append(f"Missing: {path}")
    
    # 2. Check for incorrect directories
    print("\n2. Checking for incorrect directory placement...")
    wrong_dirs = [
        project_root / "src" / "extract",
        project_root / "src" / "query",
        project_root / "src" / "io",
        project_root / "src" / "templates",
    ]
    
    found_wrong = False
    for wrong_dir in wrong_dirs:
        if wrong_dir.exists():
            print(f"    ✗ Found incorrect directory: {wrong_dir}")
            errors.append(f"Incorrect directory: {wrong_dir}")
            found_wrong = True
    
    if not found_wrong:
        print("    ✓ No incorrect directories found")
    
    # 3. Check __init__.py files
    print("\n3. Checking __init__.py files...")
    init_files = [
        project_root / "src" / "__init__.py",
        project_root / "src" / "json_extractor" / "__init__.py",
        project_root / "src" / "json_extractor" / "extract" / "__init__.py",
        project_root / "src" / "json_extractor" / "io" / "__init__.py",
        project_root / "src" / "json_extractor" / "query" / "__init__.py",
        project_root / "src" / "json_extractor" / "templates" / "__init__.py",
    ]
    
    for init_file in init_files:
        rel_path = init_file.relative_to(project_root)
        if init_file.exists():
            print(f"    ✓ {rel_path}")
        else:
            print(f"    ✗ MISSING: {rel_path}")
            errors.append(f"Missing: {rel_path}")
    
    # 4. Try importing modules
    print("\n4. Testing imports...")
    
    # Add project root to path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    test_imports = [
        ("src.json_extractor.config", "get_config"),
        ("src.json_extractor.pipeline", "run_pipeline"),
        ("src.json_extractor.io", "discover_json_files"),
        ("src.json_extractor.extract", "flatten_json_to_records"),
        ("src.json_extractor.query", "parse_filter_dsl"),
        ("src.json_extractor.templates.app_b", "AppBTemplate"),
    ]
    
    for module_name, attr_name in test_imports:
        try:
            module = __import__(module_name, fromlist=[attr_name])
            attr = getattr(module, attr_name)
            print(f"    ✓ {module_name}.{attr_name}")
        except ImportError as e:
            print(f"    ✗ Failed to import {module_name}.{attr_name}")
            print(f"       Error: {e}")
            errors.append(f"Import failed: {module_name}.{attr_name}")
        except AttributeError as e:
            print(f"    ✗ {module_name} missing {attr_name}")
            print(f"       Error: {e}")
            errors.append(f"Attribute missing: {module_name}.{attr_name}")
    
    # 5. Check dependencies
    print("\n5. Checking dependencies...")
    required_packages = [
        "pandas",
        "openpyxl",
        "typer",
        "rich",
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"    ✓ {package}")
        except ImportError:
            print(f"    ✗ MISSING: {package}")
            warnings.append(f"Missing package: {package} (run: pip install {package})")
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    if errors:
        print(f"\n❌ Found {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        print("\n💡 To fix structure issues, run: python fix_structure.py")
    else:
        print("\n✅ All structure checks passed!")
    
    if warnings:
        print(f"\n⚠️  Found {len(warnings)} warning(s):")
        for warning in warnings:
            print(f"  - {warning}")
        print("\n💡 To install dependencies, run: pip install -r requirements.txt")
    else:
        print("✅ All dependencies installed!")
    
    if not errors and not warnings:
        print("\n" + "🎉" * 20)
        print("\n✨ Installation verified successfully!")
        print("\n🚀 Ready to run:")
        print("   python cli.py --help")
        print("\n" + "🎉" * 20)
        return 0
    else:
        print("\n⚠️  Please fix the issues above before running the application.")
        return 1

if __name__ == "__main__":
    exit_code = verify_installation()
    sys.exit(exit_code)
