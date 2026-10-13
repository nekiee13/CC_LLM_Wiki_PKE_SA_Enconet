"""Project-local Appendix B sieving and query package.

The taxonomy is a template, not an approval of company scope or editions.
"""

__version__ = "0.1.0"

from .pipeline import PipelineResult, run_pipeline
from .config import Config

__all__ = ["run_pipeline", "PipelineResult", "Config"]
