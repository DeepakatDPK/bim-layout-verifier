"""BIM Layout Verifier Configuration."""
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum

@dataclass
class Config:
    """Default configuration for BIM Layout Verifier."""
    # Page normalization (1000x1000 for consistent coordinate system)
    PAGE_WIDTH_NORMALIZED = 1000.0
    PAGE_HEIGHT_NORMALIZED = 1000.0
    
    # Tolerance settings (in pixels)
    GEOMETRY_TOLERANCE = 20.0
    TEXT_TOLERANCE = 3.0
    
    # DPI settings
    DPI_RENDER = 300
    DPI_HIGH = 600
    
    # File paths
    MARKUP_DIR = "markups"
    BIM_OUTPUT_DIR = "bim_output"
    RESULTS_DIR = "results"
    
    # AI models
    USE_OCR = True
    USE_VECTOR_SIMILARITY = True
    MIN_WORD_LENGTH = 3

@dataclass
class MarkupItem:
    """Represents a single markup/comment from input."""
    id: str
    markup_type: "MarkupType"  # PDF, DWG, Image, etc.
    text: str
    position: Tuple[float, float]
    size: Tuple[float, float]
    color: Tuple[int, int, int]
    confidence: float = 1.0
    source_file: str = ""

class MarkupType(Enum):
    """Types of markup sources."""
    PDF = "pdf"
    DWG = "dwg"
    DXF = "dxf"
    IMAGE = "image"
    HAND_DRAWN = "hand_drawn"
    REVIT = "revit"
