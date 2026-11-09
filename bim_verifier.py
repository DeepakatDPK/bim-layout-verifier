"""BIM Layout Verifier - CLI and GUI Entry Point."""
import sys
import os
import argparse
from pathlib import Path

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from config import Config, MarkupItem, MarkupType
from parser import MarkupParser
from ai_engine import compare_markups, compute_geometry_similarity
from vector_store import VectorStore
from renderer import MarkupRenderer

class BIMLayoutVerifier:
    """Main verification engine."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.parser = MarkupParser(self.config)
        self.vector_store = VectorStore()
    
    def verify_layout(self, input_filepath: str, bim_output_filepath: str, tolerance: float = None) -> dict:
        """
        Verify BIM output against input markup.
        
        Args:
            input_filepath: Path to input markup file (PDF, DWG, image)
            bim_output_filepath: Path to BIM output document
            tolerance: Geometric tolerance in pixels
            
        Returns:
            dict: Verification results
        """
        tolerance = tolerance or self.config.GEOMETRY_TOLERANCE
        
        print("=" * 60)
        print("BIM Layout Verification")
        print("=" * 60)
        
        # Parse input markup
        print("\nParsing input markup: " + input_filepath)
        input_markups = self.parser.parse(input_filepath)
        print("   Found " + str(len(input_markups)) + " markups")
        
        # Parse BIM output (would extract updated markups from BIM)
        print("\nParsing BIM output: " + bim_output_filepath)
        bim_markups = self.parser.parse(bim_output_filepath)
        print("   Found " + str(len(bim_markups)) + " markups")
        
        # Store input markups for reference
        for markup in input_markups:
            self.vector_store.store(markup)
        
        # Compare markups
        print("\nComparing markups...")
        results = []
        
        for input_markup in input_markups:
            # Find matching BIM markup (by position and content)
            matching_bim = None
            for bim_markup in bim_markups:
                score, geo_type = compute_geometry_similarity(
                    input_markup, bim_markup, tolerance
                )
                if score > 0.7:
                    matching_bim = bim_markup
                    break
            
            if matching_bim:
                comparison = compare_markups(input_markup, matching_bim)
                status = comparison["status"]
                
                results.append({
                    "input_id": input_markup.id,
                    "bim_id": matching_bim.id,
                    "status": status,
                    "score": comparison["combined_score"],
                    "geometry_type": comparison["geometric_type"]
                })
                
                if status == "VERIFIED":
                    icon = "OK"
                elif status in ["PARTIAL_MATCH", "NEEDS_REVIEW"]:
                    icon = "WARN"
                else:
                    icon = "ERR"
                print("  " + icon + " " + input_markup.id + ": " + status + 
                      " (score: {:.2f})".format(comparison["combined_score"]))
            else:
                # Missing markup
                results.append({
                    "input_id": input_markup.id,
                    "bim_id": None,
                    "status": "MISSING",
                    "score": 0.0,
                    "geometry_type": "NO_MATCH"
                })
                print("  WARN " + input_markup.id + ": MISSING in BIM output")
        
        # Summary
        print("\n" + "=" * 60)
        print("Verification Summary")
        print("=" * 60)
        
        verified = len([r for r in results if r["status"] == "VERIFIED"])
        partial = len([r for r in results if r["status"] in ["PARTIAL_MATCH", "NEEDS_REVIEW"]])
        missing = len([r for r in results if r["status"] in ["MISSING", "MISMATCH"]])
        total = len(results)
        
        print("  Total:   " + str(total))
        print("  OK:      " + str(verified))
        print("  Partial: " + str(partial))
        print("  Missing: " + str(missing))
        
        return {
            "verified": verified,
            "partial": partial,
            "missing": missing,
            "total": total,
            "results": results
        }

def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="BIM Layout Verifier - Compare input markups with BIM output"
    )
    parser.add_argument("--input", "-i", required=True, 
                        help="Input markup file (PDF, DWG, image)")
    parser.add_argument("--bim", "-b", required=True,
                        help="BIM output file")
    parser.add_argument("--tolerance", "-t", type=float, default=20.0,
                        help="Geometric tolerance in pixels (default: 20)")
    parser.add_argument("--gui", action="store_true",
                        help="Launch GUI visualization")
    
    args = parser.parse_args()
    
    if args.gui:
        app = MarkupRenderer()
        app.show()
        sys.exit(app.exec())
    else:
        verifier = BIMLayoutVerifier()
        results = verifier.verify_layout(
            input_filepath=args.input,
            bim_output_filepath=args.bim,
            tolerance=args.tolerance
        )
        
        # Exit with appropriate code
        if results["missing"] > 0:
            sys.exit(1)
        sys.exit(0)

if __name__ == "__main__":
    main()
