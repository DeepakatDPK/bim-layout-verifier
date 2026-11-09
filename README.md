# BIM Layout Verifier

AI-powered BIM markup verification tool that compares input markups with BIM output using intelligent detection and vector-based semantic search.

## Features

- 🤖 AI-powered markup detection and comparison
- 📐 Layout parser with high-precision rendering
- 🔍 Vector store for semantic similarity search
- ⚡ Python 3.14+ compatible, standalone execution
- 📊 Detailed comparison reports with visual output

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the verifier
python bim_verifier.py --input markup_input.txt --bim-output bim_output.txt
```

## Project Structure

```
bim_layout_verifier/
├── __init__.py          # Package initialization
├── bim_verifier.py      # Core verification engine
├── ai_engine.py         # AI-powered markup detection
├── parser.py            # Layout parser
├── renderer.py          # Output renderer
├── config.py            # Configuration management
├── vector_store.py      # Vector store for semantic search
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.py` to customize:
- AI model parameters
- Comparison thresholds
- Output formats
- Vector store settings

## Usage Examples

### Basic Verification
```bash
python bim_verifier.py --input layout_input.txt --bim-output model_output.txt
```

### With Detailed Reports
```bash
python bim_verifier.py --input layout_input.txt --bim-output model_output.txt --report detailed
```

### Custom AI Engine
```bash
python bim_verifier.py --input layout_input.txt --bim-output model_output.txt --engine neural
```

## Technical Details

- **Input Format:** Standard markup text files with layer/element definitions
- **Output Format:** BIM model comparison reports in JSON/Markdown
- **AI Integration:** Uses vector embeddings for semantic similarity matching
- **Performance:** Optimized for A0 paper scale at 2400 DPI resolution

## License

MIT License - See LICENSE file for details.

## Contact

Author: Deepak George  
Email: deepak.george@example.com  
GitHub: https://github.com/DeepakatDPK/bim-layout-verifier
