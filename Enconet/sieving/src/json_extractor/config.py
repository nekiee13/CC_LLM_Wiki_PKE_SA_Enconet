# ------------------------
# src/json_extractor/config.py
# ------------------------
"""
Configuration management for JSON Extractor vNext.

Handles:
- Default column selections
- User preference persistence
- Canonical taxonomy definitions
- File path management
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class Config:
    """Application configuration."""
    
    # Directories
    data_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parents[2] / "DATA")
    config_dir: Path = field(default_factory=lambda: Path.home() / ".json_extractor")
    
    # Default column selection (essential subset)
    default_columns: List[str] = field(default_factory=lambda: [
        "record_side",
        "criterion_id",
        "criterion_name",
        "item_type",
        "statement",
        "evidence_quote_1",
        "doc_id",
        "filename",
        "title",
        "rule_key",
        "rule_ref_keys",
        "rule_strength",
    ])
    
    # All canonical fields (stable schema order)
    all_columns: List[str] = field(default_factory=lambda: [
        "template_id",
        "template_version",
        "taxonomy_id",
        "record_side",
        "doc_id",
        "filename",
        "title",
        "revision",
        "item_id",
        "item_type",
        "criterion_id",
        "criterion_name",
        "statement",
        "evidence_quote_1",
        "evidence_quotes_json",
        "source_page",
        "source_page_label",
        "source_heading_path",
        "source_section_id",
        "source_block_type",
        "source_location_cue",
        "entities_organizations",
        "entities_people",
        "entities_documents",
        "entities_systems_tools",
        "entities_standards_regulations",
        "rule_source_rules",
        "rule_locator",
        "rule_key",
        "rule_strength",
        "rule_citation_text",
        "rule_ref_keys",
        "rule_ref_codes",
        "rule_ref_locators",
        "rule_ref_texts_json",
    ])
    
    def __post_init__(self):
        """Ensure config directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    @property
    def column_defaults_path(self) -> Path:
        """Path to saved column defaults."""
        return self.config_dir / "column_defaults.json"
    
    def load_column_defaults(self) -> List[str]:
        """
        Load user's saved column preferences.
        
        Returns:
            List of column names, or default_columns if no saved preferences.
        """
        if self.column_defaults_path.exists():
            try:
                with open(self.column_defaults_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    columns = data.get("columns", self.default_columns)
                    # Validate columns exist in all_columns
                    valid_columns = [c for c in columns if c in self.all_columns]
                    return valid_columns if valid_columns else self.default_columns
            except Exception as e:
                print(f"Warning: Could not load column defaults: {e}")
                return self.default_columns
        return self.default_columns
    
    def save_column_defaults(self, columns: List[str]) -> None:
        """
        Save user's column preferences.
        
        Args:
            columns: List of column names to save as default.
        """
        try:
            # Validate columns
            valid_columns = [c for c in columns if c in self.all_columns]
            
            data = {
                "columns": valid_columns,
                "version": "0.1",
            }
            
            with open(self.column_defaults_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            print(f"✓ Saved {len(valid_columns)} columns as default to {self.column_defaults_path}")
        
        except Exception as e:
            print(f"Error saving column defaults: {e}")
    
    def get_canonical_criteria(self) -> List[Dict[str, str]]:
        """
        Get the canonical Appendix B criteria table.
        
        Returns:
            List of dicts with criterion_id and criterion_name.
        """
        return [
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
    
    def get_canonical_codes(self) -> List[Dict[str, Any]]:
        """
        Get the canonical rule code table.
        
        Returns:
            List of canonical ref_code definitions.
        """
        return [
            {
                "ref_code": "10CFR50_APPB",
                "ref_type": "REGULATION",
                "title": "10 CFR Part 50 Appendix B — Quality Assurance Criteria for Nuclear Power Plants and Fuel Reprocessing Plants",
                "allowed_locators": [f"APP_B_{rom}" for rom in ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII"]],
            },
            {
                "ref_code": "10CFR21",
                "ref_type": "REGULATION",
                "title": "10 CFR Part 21 — Reporting of Defects and Noncompliance",
                "locator_pattern": r"^21\.[0-9]+$",
            },
        ]
    
    def criterion_name_for_id(self, criterion_id: str) -> Optional[str]:
        """
        Get canonical criterion name for a criterion_id.
        
        Args:
            criterion_id: e.g., "APP_B_I"
        
        Returns:
            Canonical name or None if not found.
        """
        for criterion in self.get_canonical_criteria():
            if criterion["criterion_id"] == criterion_id:
                return criterion["criterion_name"]
        return None


# Global singleton instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create the global Config singleton."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def set_config(config: Config) -> None:
    """Set the global Config singleton (for testing)."""
    global _config
    _config = config
