"""AI-Powered Markup Comparison Engine."""
import numpy as np
from typing import List, Tuple
from .config import MarkupItem

def compute_geometry_similarity(
    item1: MarkupItem,
    item2: MarkupItem,
    tolerance: float = 20.0
) -> Tuple[float, str]:
    """
    Compute spatial and geometric similarity between two markups.
    
    Returns:
        (similarity_score, match_type)
    """
    # Compute position difference
    pos_diff_x = abs(item1.position[0] - item2.position[0])
    pos_diff_y = abs(item1.position[1] - item2.position[1])
    
    # Normalize to page size
    max_dist = 1000.0
    pos_similarity = max(0, 1 - (max(pos_diff_x, pos_diff_y) / max_dist))
    
    # Compute size similarity
    size_diff_x = abs(item1.size[0] - item2.size[0])
    size_diff_y = abs(item1.size[1] - item2.size[1])
    
    max_size = 500.0
    size_similarity = max(0, 1 - (max(size_diff_x, size_diff_y) / max_size))
    
    # Combined geometric score
    geometric_score = 0.6 * pos_similarity + 0.4 * size_similarity
    
    # Classify match type
    if geometric_score > 0.85:
        match_type = "EXACT_MATCH"
    elif geometric_score > 0.70:
        match_type = "NEAR_MATCH"
    elif geometric_score > 0.50:
        match_type = "PARTIAL_MATCH"
    else:
        match_type = "NO_MATCH"
    
    return geometric_score, match_type

def compute_text_similarity(text1: str, text2: str, tolerance: float = 3.0) -> float:
    """
    Simple text similarity (Levenshtein distance).
    In production: use fuzzywuzzy or difflib.
    """
    if not text1 or not text2:
        return 0.0
    
    # Normalize
    t1 = text1.lower().strip()
    t2 = text2.lower().strip()
    
    # Simple character-based similarity
    max_len = max(len(t1), len(t2))
    if max_len == 0:
        return 1.0
    
    matches = 0
    for c1, c2 in zip(t1, t2):
        if c1 == c2:
            matches += 1
    
    similarity = matches / max_len
    return similarity

def compare_markups(input_markup: MarkupItem, bim_markup: MarkupItem) -> dict:
    """
    Full comparison between input and BIM output markup.
    """
    geo_score, geo_type = compute_geometry_similarity(input_markup, bim_markup)
    text_score = compute_text_similarity(input_markup.text, bim_markup.text)
    
    # Combined score (geometry weighted higher)
    combined_score = 0.7 * geo_score + 0.3 * text_score
    
    # Determine status
    if combined_score > 0.85 and geo_type in ["EXACT_MATCH", "NEAR_MATCH"]:
        status = "VERIFIED"
    elif combined_score > 0.70:
        status = "PARTIAL_MATCH"
    elif combined_score > 0.50:
        status = "NEEDS_REVIEW"
    else:
        status = "MISMATCH"
    
    return {
        "status": status,
        "geometric_score": geo_score,
        "geometric_type": geo_type,
        "text_similarity": text_score,
        "combined_score": combined_score
    }
