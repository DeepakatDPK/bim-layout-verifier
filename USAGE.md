# USAGE.md

# BIM Layout Verifier - Comprehensive Usage Guide

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [Basic Usage](#basic-usage)
3. [Advanced Configuration](#advanced-configuration)
4. [Input File Formats](#input-file-formats)
5. [Output Report Interpretation](#output-report-interpretation)
6. [Performance Tuning](#performance-tuning)
7. [Integration Patterns](#integration-patterns)
8. [Troubleshooting](#troubleshooting)

---

## Quick Reference

| Task | Command |
|------|---------|
| Verify markups | `python bim_verifier.py -i input.txt -o result.json` |
| Detailed markdown report | `python bim_verifier.py -i input.txt -r markdown -v` |
| Neural engine | `python bim_verifier.py -i input.txt -e neural -t 0.95` |
| Parallel processing | `python bim_verifier.py -i input.txt -j 8` |
| Custom config | `python bim_verifier.py -c config.yaml -i input.txt` |
| Batch verification | `for f in inputs/*.txt; do python bim_verifier.py -i "$f"; done` |
| API usage | `from bim_verifier import BIMVerifier; verifier = BIMVerifier()` |

---

## Basic Usage

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Prepare Input File

Create `input.txt`:

```text
LAYER_001: Exterior_Wall
  POSITION: 0.0, 0.0
  DIMENSION: 15000 x 4500
  MATERIAL: Reinforced_Concrete

LAYER_002: Interior_Column
  POSITION: 3000.0, 3000.0
  DIMENSION: 600 x 600
  MATERIAL: Steel
```

### Step 3: Run Verification

```bash
# Basic verification
python bim_verifier.py -i input.txt

# With output file
python bim_verifier.py -i input.txt -o verification.json

# With detailed report
python bim_verifier.py -i input.txt -o report.md -r markdown
```

### Expected Output

```text
✅ Verification complete!
  - Markups verified: 2
  - Matches found: 2
  - Discrepancies: 0
  - Confidence score: 98.7%

📊 Report saved to: verification.json
```

---

## Advanced Configuration

### Command-Line Options

```bash
python bim_verifier.py --help
```

| Option | Description | Example |
|--------|-------------|---------|
| `-i, --input FILE` | Input markup file | `-i layout.txt` |
| `-o, --output FILE` | Output file path | `-o result.json` |
| `-r, --report FORMAT` | Output format | `-r markdown` |
| `-e, --engine TYPE` | AI engine type | `-e neural` |
| `-t, --threshold FLOAT` | Match confidence threshold | `-t 0.9` |
| `-j, --threads INT` | Worker threads | `-j 4` |
| `-v, --verbose` | Verbose output | `-v` |
| `-c, --config FILE` | Config file path | `-c config.yaml` |

### Configuration File (config.yaml)

```yaml
verification:
  threshold: 0.85
  strict_mode: false
  output_format: json
  batch_size: 100

ai:
  engine: vector
  model_path: ./models/bim_embeddings.bin
  enable_caching: true

performance:
  max_workers: 4
  batch_size: 100
  enable_parallel_embedding: true

logging:
  level: INFO
  file: verifier.log
```

### Environment Variables

```bash
# Set before running
export BIM_VERIFIER_LOG_LEVEL=DEBUG
export BIM_VERIFIER_VECTOR_DIM=1536
export BIM_VERIFIER_MAX_THREADS=8
export BIM_VERIFIER_CACHE_DIR=/tmp/bim_cache
```

---

## Input File Formats

### Standard Format

```text
# Comments start with #
LAYER_ID: identifier
  POSITION: x, y
  DIMENSION: width x height
  MATERIAL: material_name
  [OPTIONAL: additional fields]
```

### Supported Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `LAYER_ID` | String | Yes | Unique identifier |
| `POSITION` | Float | Yes | X, Y coordinates |
| `DIMENSION` | Float | Yes | Width x height |
| `MATERIAL` | String | Yes | Material type |
| `COLOR` | String | No | Visual identifier |
| `NOTE` | String | No | Additional notes |

### Example: Complex Project

```text
# Building A - Ground Floor Plan
LAYER_A1: Exterior_North_Wall
  POSITION: 0.0, 0.0
  DIMENSION: 20000 x 12000
  MATERIAL: Reinforced_Concrete
  COLOR: #808080
  NOTE: Primary facade

LAYER_A2: Interior_Column_Grid
  POSITION: 5000.0, 5000.0
  DIMENSION: 800 x 800
  MATERIAL: Steel_Rebar
  ID: COL_GRID_001

LAYER_A3: Door_Assembly
  POSITION: 12000.0, 6000.0
  DIMENSION: 1500 x 2400
  MATERIAL: Glass_Sliding
  NOTE: Main entrance
```

### Batch Input

For multiple files, use wildcard expansion:

```bash
# Linux/Mac
python bim_verifier.py -i "floor_*/layout.txt" -o batch_result.json

# Windows
python bim_verifier.py -i "floor_*\layout.txt" -o batch_result.json
```

---

## Output Report Interpretation

### JSON Report Structure

```json
{
  "verification_id": "ver_20261109_120833",
  "timestamp": "2026-11-09T12:08:33Z",
  "summary": {
    "total_markups": 10,
    "verified": 10,
    "matched": 10,
    "discrepancies": 0,
    "confidence_score": 98.7,
    "processing_time_ms": 245
  },
  "details": [
    {
      "markup_id": "LAYER_A1",
      "bim_match": "Exterior_North_Wall",
      "confidence": 0.98,
      "status": "verified",
      "position_match": true,
      "dimension_match": true
    }
  ],
  "statistics": {
    "average_confidence": 0.96,
    "min_confidence": 0.89,
    "max_confidence": 0.99,
    "match_distribution": {
      "exact": 6,
      "semantic": 3,
      "positional": 1
    }
  }
}
```

### Status Codes

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| `verified` | Perfect match | None |
| `matched_semantic` | High confidence semantic match | Review if strict mode |
| `positional_only` | Position match, weak content | Verify material/type |
| `discrepancy` | Low confidence or mismatch | Investigate |
| `unmatched` | No match found | Check input data |

### Markdown Report Example

```markdown
# BIM Verification Report

**Verification ID:** ver_20261109_120833  
**Timestamp:** 2026-11-09 12:08:33 UTC  
**Status:** ✅ PASSED

## Summary
- Total Markups: 10
- Verified: 10
- Matches: 10
- Confidence Score: 98.7%

## Details
| Markup | BIM Match | Confidence | Status |
|--------|-----------|------------|--------|
| LAYER_A1 | Exterior_North_Wall | 98% | ✅ Verified |
| LAYER_A2 | Interior_Column_Grid | 96% | ✅ Verified |

## Recommendations
- No discrepancies found
- All markups within acceptable tolerance
- Proceed with next verification stage
```

---

## Performance Tuning

### Multi-Threading

```bash
# Single-threaded (baseline)
python bim_verifier.py -i large_input.txt

# 4 workers (recommended)
python bim_verifier.py -i large_input.txt -j 4

# 8 workers (maximal)
python bim_verifier.py -i large_input.txt -j 8
```

### Configuration Tuning

```yaml
# config.yaml
performance:
  max_workers: 8
  batch_size: 256  # Process 256 elements per batch
  enable_parallel_embedding: true
  enable_caching: true
```

### Caching Strategy

```python
# Enable vector caching for repeated queries
from vector_store import VectorStore

vector_store = VectorStore(enable_caching=True, cache_dir="/tmp/bim_cache")
```

### Memory Optimization

- Use `--threshold 0.9` to reduce false positives
- Limit batch size for large datasets: `batch_size: 64`
- Use single-threaded mode for memory-constrained environments

---

## Integration Patterns

### Python API Integration

```python
# In your application
from bim_verifier import BIMVerifier
from parser import LayoutParser
import json

def verify_markups(input_path, output_path=None):
    parser = LayoutParser()
    verifier = BIMVerifier()
    
    # Parse input
    markups = parser.parse_file(input_path)
    
    # Verify
    results = verifier.verify(markups)
    
    # Export results
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(results.to_dict(), f, indent=2)
    
    return results

# Usage
results = verify_markups("layout.txt", "results.json")
print(f"Verification complete: {results.summary['verified']}/{results.summary['total_markups']}")
```

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/verify.yml
name: BIM Verification

on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.14'
      - run: pip install -r requirements.txt
      - run: python bim_verifier.py -i tests/fixtures/sample.txt -o /dev/null
      - run: pytest
```

### Docker Integration

```dockerfile
# Dockerfile
FROM python:3.14-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Runtime
CMD ["python", "bim_verifier.py", "-i", "/input/layout.txt", "-o", "/output/result.json"]
```

---

## Troubleshooting

### Common Issues

#### Issue: "No module named 'bim_verifier'"
```bash
# Solution: Install from source
cd bim_layout_verifier
pip install -e .
```

#### Issue: "Threshold too low - many false matches"
```bash
# Solution: Increase threshold
python bim_verifier.py -t 0.95  # Higher = stricter matching
```

#### Issue: "Verification too slow"
```bash
# Solution: Enable parallel processing
python bim_verifier.py -j 8  # Use 8 worker threads
```

#### Issue: "Memory error on large files"
```bash
# Solution: Reduce batch size and workers
python bim_verifier.py -j 2 --batch-size 64
```

#### Issue: "Position tolerance too strict"
```python
# Solution: Adjust tolerance in config.py
TOLERANCE_METERS = 0.05  # Increased from 0.01
```

### Debug Mode

```bash
# Enable debug logging
export BIM_VERIFIER_LOG_LEVEL=DEBUG
python bim_verifier.py -i input.txt -v
```

### Getting Help

- Check documentation: `cat README.md`
- View examples: `ls examples/`
- Report issues: [GitHub Issues](https://github.com/DeepakatDPK/bim-layout-verifier/issues)
