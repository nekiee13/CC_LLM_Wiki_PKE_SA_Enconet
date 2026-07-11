# ------------------------
# src/json_extractor/templates/app_b.py
# ------------------------
"""
Appendix B (10 CFR 50) template definition.

Provides template metadata, controlled vocabularies, and template-specific utilities.
"""

from typing import Dict, List, Any


class AppBTemplate:
    """
    JSON_Template_App_B definition.
    
    Provides:
    - Template metadata
    - Canonical criteria table
    - Canonical rule codes
    - Controlled vocabularies for enums
    """
    
    TEMPLATE_ID = "JSON_Template_App_B"
    TEMPLATE_VERSION = "0.1"
    TAXONOMY_ID = "APP_B"
    
    # Canonical 18 criteria
    CRITERIA = [
        {"criterion_id": "APP_B_I", "criterion_name": "Organization"},
        {"criterion_id": "APP_B_II", "criterion_name": "Quality Assurance Program"},
        {"criterion_id": "APP_B_III", "criterion_name": "Design Control"},
        {"criterion_id": "APP_B_IV", "criterion_name": "Procurement Document Control"},
        {"criterion_id": "APP_B_V", "criterion_name": "Instructions, Procedures, and Drawings"},
        {"criterion_id": "APP_B_VI", "criterion_name": "Document Control"},
        {"criterion_id": "APP_B_VII", "criterion_name": "Control of Purchased Material, Equipment, and Services"},
        {"criterion_id": "APP_B_VIII", "criterion_name": "Identification and Control of Materials, Parts, and Components"},
        {"criterion_id": "APP_B_IX", "criterion_name": "Control of Special Processes"},
        {"criterion_id": "APP_B_X", "criterion_name": "Inspection"},
        {"criterion_id": "APP_B_XI", "criterion_name": "Test Control"},
        {"criterion_id": "APP_B_XII", "criterion_name": "Control of Measuring and Test Equipment"},
        {"criterion_id": "APP_B_XIII", "criterion_name": "Handling, Storage, and Shipping"},
        {"criterion_id": "APP_B_XIV", "criterion_name": "Inspection, Test, and Operating Status"},
        {"criterion_id": "APP_B_XV", "criterion_name": "Nonconforming Materials, Parts, or Components"},
        {"criterion_id": "APP_B_XVI", "criterion_name": "Corrective Action"},
        {"criterion_id": "APP_B_XVII", "criterion_name": "Quality Assurance Records"},
        {"criterion_id": "APP_B_XVIII", "criterion_name": "Audits"},
    ]
    
    # Canonical rule codes
    CANONICAL_CODES = [
        {
            "ref_code": "10CFR50_APPB",
            "ref_type": "REGULATION",
            "title": "10 CFR Part 50 Appendix B — Quality Assurance Criteria for Nuclear Power Plants and Fuel Reprocessing Plants",
        },
        {
            "ref_code": "10CFR21",
            "ref_type": "REGULATION",
            "title": "10 CFR Part 21 — Reporting of Defects and Noncompliance",
        },
    ]
    
    # Enums
    RECORD_SIDE_VALUES = ["RULE", "DOCUMENT"]
    RULE_STRENGTH_VALUES = ["MANDATORY", "NON_MANDATORY"]
    
    ITEM_TYPE_VALUES = [
        "requirement",
        "process_step",
        "role_responsibility",
        "definition",
        "control",
        "record",
        "reference",
        "finding",
        "recommendation",
        "action",
        "status_statement",
        "other",
    ]
    
    @classmethod
    def get_criterion_ids(cls) -> List[str]:
        """Get list of valid criterion IDs."""
        return [c["criterion_id"] for c in cls.CRITERIA]
    
    @classmethod
    def get_criterion_names(cls) -> List[str]:
        """Get list of valid criterion names."""
        return [c["criterion_name"] for c in cls.CRITERIA]
    
    @classmethod
    def get_criterion_map(cls) -> Dict[str, str]:
        """Get mapping of criterion_id → criterion_name."""
        return {c["criterion_id"]: c["criterion_name"] for c in cls.CRITERIA}
    
    @classmethod
    def get_ref_codes(cls) -> List[str]:
        """Get list of valid ref_code values."""
        return [c["ref_code"] for c in cls.CANONICAL_CODES]
    
    @classmethod
    def validate_criterion_id(cls, criterion_id: str) -> bool:
        """Check if criterion_id is valid."""
        return criterion_id in cls.get_criterion_ids()
    
    @classmethod
    def validate_criterion_name(cls, criterion_id: str, criterion_name: str) -> bool:
        """Check if criterion_name matches criterion_id."""
        criterion_map = cls.get_criterion_map()
        return criterion_map.get(criterion_id) == criterion_name
