"""Keep readable company identity distinct from safe artifact filename stems."""
import re


def supplier_label(value):
    if (not isinstance(value,str) or not value.strip() or value != value.strip()
            or len(value)>256 or any(ord(c)<32 or 127<=ord(c)<160 for c in value)):
        raise ValueError('Supplier must be a non-empty printable local company name')
    return value


def filename_stem(value):
    return re.sub(r'[^a-z0-9_-]+','-',supplier_label(value).casefold()).strip('-') or 'vendor'
