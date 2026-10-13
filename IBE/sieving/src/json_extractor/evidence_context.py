"""Validate optional source anchors without guessing missing values."""
from datetime import date
from pathlib import Path

import yaml

CONTRACT=Path(__file__).resolve().parents[3]/'schemas/evidence_context.yml'


def validate_context(item):
    spec=yaml.safe_load(CONTRACT.read_text(encoding='utf-8'))
    errors=[]
    if 'evidence_type' in item and item['evidence_type'] not in spec['evidence_types']:
        errors.append('evidence_type: unknown value')
    if 'context' not in item:
        return errors
    context=item['context']
    if not isinstance(context,dict):
        return errors+['context: must be an object when supplied']
    for field,value in context.items():
        if field not in spec['context_fields']:
            errors.append('context: unknown field '+field)
        elif not isinstance(value,str) or not value.strip():
            errors.append('context.'+field+': non-empty string required when supplied')
        elif field=='evidence_date' and value!='n-a':
            try:
                if date.fromisoformat(value).isoformat()!=value:
                    raise ValueError()
            except ValueError:
                errors.append('context.evidence_date: ISO date or n-a required')
    return errors
