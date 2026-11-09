# CONTRIBUTING.md

# Contributing to BIM Layout Verifier

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Commit Guidelines](#commit-guidelines)
6. [Pull Request Process](#pull-request-process)
7. [Architecture Changes](#architecture-changes)
8. [Reporting Issues](#reporting-issues)

---

## Code of Conduct

### Our Promise

We aim to be an inclusive, welcoming community. We pledge to:

- **Be respectful**: Listen to others with openness and empathy
- **Be constructive**: Focus on technical solutions and clear communication
- **Be welcoming**: Make everyone feel safe and valued
- **Be responsible**: Own your contributions and help others learn

### Guidelines

- Use professional and inclusive language
- Welcome new contributors with patience and encouragement
- Accept constructive criticism and feedback gracefully
- Focus on what is best for the community and project

---

## How to Contribute

### Types of Contributions

| Category | Examples |
|----------|----------|
| 🐛 Bug Fixes | Fix parsing errors, improve performance, resolve crashes |
| ✨ New Features | Add new AI engines, output formats, or parser extensions |
| 📚 Documentation | Improve README, add examples, clarify API docs |
| 🧪 Tests | Write unit tests, edge case coverage, integration tests |
| 🔧 Refactoring | Improve code structure, add type hints, optimize algorithms |
| 📝 Translations | Localize documentation or error messages |

### Quick Contribution Checklist

Before submitting, ensure your contribution:

- [ ] Solves a real problem or adds clear value
- [ ] Follows the project's coding standards (see below)
- [ ] Includes appropriate tests (if applicable)
- [ ] Has working examples or documentation updates
- [ ] Passes all existing tests
- [ ] Includes a clear commit message
- [ ] Addresses an open issue or creates a relevant one

---

## Development Setup

### Prerequisites

- Git (version 2.30+)
- Python 3.14 or higher
- pip and virtualenv
- Optional: pytest, black, mypy, pre-commit

### Step-by-Step Setup

#### 1. Fork and Clone

```bash
# Fork the repository on GitHub
git clone https://github.com/YOUR_USERNAME/bim-layout-verifier.git
cd bim-layout-verifier
```

#### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Development Dependencies

```bash
# Install in editable mode with dev extras
pip install -e ".[dev]"

# Or install manually
pip install -r requirements.txt
pip install pytest pytest-cov black mypy pre-commit
```

#### 4. Verify Installation

```bash
# Run tests to ensure everything works
pytest

# Lint the code
black --check .

# Type-check
mypy .
```

#### 5. Set Up Pre-commit Hooks (Recommended)

```bash
# Install pre-commit
pip install pre-commit

# Initialize hooks
pre-commit install

# Run hooks on all files
pre-commit run --all-files
```

---

## Coding Standards

### Python Style Guide

We follow **PEP 8** with these additional rules:

#### File Structure

```
bim_layout_verifier/
├── __init__.py          # Package initialization
├── bim_verifier.py      # Main module
├── ai_engine.py         # AI logic
├── parser.py            # Parsing logic
├── vector_store.py      # Vector embeddings
├── renderer.py          # Output formatting
├── config.py            # Configuration
├── tests/               # Test suite
├── examples/            # Example files
└── docs/                # Documentation
```

#### Naming Conventions

- **Classes**: `PascalCase` (e.g., `BIMVerifier`, `LayoutParser`)
- **Functions/Methods**: `snake_case` (e.g., `parse_file`, `verify_markup`)
- **Variables**: `snake_case` (e.g., `markup_list`, `confidence_score`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_THREADS`, `DEFAULT_THRESHOLD`)
- **Private**: Prefix with `_` (e.g., `_internal_helper`, `_config`)

#### Type Hints

All public functions and methods should include type hints:

```python
from typing import List, Tuple, Optional

def parse_markup_file(filepath: str) -> List[MarkupElement]:
    """Parse a markup file and return list of elements."""
    ...

def verify(markup: MarkupElement, threshold: float = 0.85) -> bool:
    """Verify a single markup element."""
    ...
```

#### Docstrings

Use Google-style docstrings:

```python
def parse_file(filepath: str) -> List[MarkupElement]:
    """
    Parse a markup file and extract layout elements.

    Args:
        filepath: Path to the markup file to parse.

    Returns:
        List of MarkupElement objects extracted from the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ParseError: If the file contains invalid markup syntax.
    """
    ...
```

### Code Quality Tools

- **Black**: Auto-format code
- **isort**: Sort imports
- **mypy**: Static type checking
- **flake8**: Linting

Example CI configuration:

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.14'
      - run: pip install black mypy pytest
      - run: black --check .
      - run: mypy .
      - run: pytest --cov=.
```

---

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(parser): add support for CSV input` |
| `fix` | Bug fix | `fix(ai_engine): resolve off-by-one error in indexing` |
| `docs` | Documentation only | `docs(README): add installation instructions` |
| `style` | Formatting, missing semi-colons | `style(bim_verifier.py): add missing type hints` |
| `refactor` | Code change that neither fixes nor adds | `refactor(vector_store): extract embedding generation` |
| `perf` | Performance improvement | `perf(verification): reduce memory usage by 30%` |
| `test` | Adding tests | `test(parser): add edge case coverage for unicode` |
| `chore` | Maintenance tasks | `chore: update dependencies to latest versions` |

#### Subject

- Use present tense ("add feature" not "added feature")
- Keep it concise (50 chars max)
- Capitalize first letter, no period at end

#### Body

- Explain **why** and **how**, not **what**
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- Wrap at 72 characters

#### Example

```
feat(ai_engine): add neural network backend

Implement a neural network-based classification engine as an alternative
to the vector embedding approach. This provides better accuracy for
complex markup patterns while maintaining backward compatibility.

- Added NeuralEngine class in ai_engine.py
- Updated EngineRegistry to include NEURAL type
- Added tests in tests/test_neural_engine.py
- Performance: ~15% slower but 2x accuracy on complex inputs
```

---

## Pull Request Process

### Before Submitting

1. **Create a branch from `main`**:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes** with clear, focused commits

3. **Run the test suite**:
   ```bash
   pytest
   ```

4. **Run linting**:
   ```bash
   black .
   mypy .
   ```

5. **Update documentation** if necessary

6. **Write a clear commit message** following the guidelines above

### PR Template

When opening a PR, fill out these sections:

```markdown
## Description

Brief description of the changes and the problem they solve.

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing

Describe how you tested these changes:
- [ ] Unit tests added
- [ ] Integration tests updated
- [ ] Manual testing performed
- [ ] Edge cases considered

## Checklist

- [ ] Code follows the style guide
- [ ] Code is well-documented
- [ ] All tests pass
- [ ] No new warnings introduced
- [ ] Documentation updated (if applicable)
- [ ] Examples provided (if applicable)
```

### Review Process

1. **Automated Checks**: CI will run tests, linting, and type checking
2. **Maintainer Review**: A maintainer will review within 3-5 business days
3. **Feedback**: You may be asked to make changes or provide clarification
4. **Merge**: Once approved, a maintainer will merge your PR

---

## Architecture Changes

### When to Propose Architecture Changes

Significant architectural changes require a design document:

- New module structure
- Major algorithm changes
- Database/vector store migration
- API contract changes
- Performance-critical optimizations

### Design Document Template

```markdown
# Design: [Feature/Change Name]

## Problem Statement
Describe the problem or opportunity this change addresses.

## Proposed Solution
High-level description of the approach.

## Alternatives Considered
Briefly describe other approaches and why they were rejected.

## Impact Analysis
- **Performance**: Expected improvements or regressions
- **Compatibility**: Backward compatibility considerations
- **Risk**: Potential failure modes and mitigation
- **Rollback**: How to revert if needed

## Implementation Plan
1. Phase 1: Foundation
2. Phase 2: Core functionality
3. Phase 3: Testing and validation

## Metrics for Success
How will we measure whether this change was successful?
```

---

## Reporting Issues

### Bug Reports

Include these details:

- [ ] Clear description of the bug
- [ ] Steps to reproduce (exact commands, input files)
- [ ] Expected behavior
- [ ] Actual behavior
- [ ] Python version (`python --version`)
- [ ] OS and architecture
- [ ] Error messages (full stack trace if applicable)
- [ ] Input file sample (if relevant)

### Feature Requests

Describe:

- [ ] The use case and problem statement
- [ ] Proposed solution or improvement
- [ ] Priority and expected impact
- [ ] Any relevant examples or references

### How to Report

1. Check existing issues to avoid duplicates
2. Use the issue template if provided
3. Be concise but thorough
4. Label appropriately (bug, enhancement, question, etc.)

---

## Getting Help

- **Documentation**: Check README.md and inline docstrings
- **Issues**: Search existing issues on GitHub
- **Discussions**: Join conversations on the project page
- **Direct Contact**: deepak.george@example.com (for major contributions)

---

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License (same as the main project).

---

<div align="center">

**Thank you for contributing to BIM Layout Verifier!**

[![Stars](https://img.shields.io/github/stars/DeepakatDPK/bim-layout-verifier?style=social)](https://github.com/DeepakatDPK/bim-layout-verifier/stargazers)
[![Forks](https://img.shields.io/github/forks/DeepakatDPK/bim-layout-verifier?style=social)](https://github.com/DeepakatDPK/bim-layout-verifier/network/members)

</div>
