# ------------------------
# fix_init_files.py
# ------------------------
#!/usr/bin/env python3
"""
Fix all __init__.py files to include proper exports.

Run from project root: python fix_init_files.py
"""

from pathlib import Path

def fix_io_init():
    """Fix src/json_extractor/io/__init__.py"""
    content = '''"""
I/O operations: file discovery, reading, and export.
"""

from .files import discover_json_files, read_json_file, BadFileReport
from .export import export_to_csv, export_to_xlsx, export_dataframe

__all__ = [
    "discover_json_files",
    "read_json_file",
    "BadFileReport",
    "export_to_csv",
    "export_to_xlsx",
    "export_dataframe",
]
'''
    path = Path("src/json_extractor/io/__init__.py")
    path.write_text(content, encoding='utf-8')
    print(f"✓ Fixed {path}")

def fix_query_init():
    """Fix src/json_extractor/query/__init__.py"""
    content = '''"""
Query system: schema, DSL compiler, and execution engine.
"""

from .schema import QuerySchema, FieldDef
from .compiler import parse_filter_dsl, QueryFilter, CompiledQuery
from .engine import QueryEngine

__all__ = [
    "QuerySchema",
    "FieldDef",
    "parse_filter_dsl",
    "QueryFilter",
    "CompiledQuery",
    "QueryEngine",
]
'''
    path = Path("src/json_extractor/query/__init__.py")
    path.write_text(content, encoding='utf-8')
    print(f"✓ Fixed {path}")

def main():
    print("Fixing __init__.py files...")
    print("=" * 60)
    
    try:
        fix_io_init()
        fix_query_init()
        
        print("=" * 60)
        print("✅ All __init__.py files fixed!")
        print("\nYou can now run:")
        print("  streamlit run app.py")
        print("  python cli.py --help")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
