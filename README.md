# Deckflow

Programmatic PowerPoint presentation management. Deckflow enables you to extract, analyze, and modify the content of PPTX files in a simple and intuitive way.

## Installation

```bash
pip install deckflow
```

**Requirements:** Python 3.9+

## Features

- Content extraction (text, tables, charts)
- Formatting properties analysis
- Element modification and updates
- Duplicate detection support

## Quick Start

```python
from deckflow import Deck

# Load a presentation
deck = Deck("presentation.pptx")

# Access slides
for slide in deck.slides:
    print(slide)
```

## Project Status

⚠️ Version 0.1.0 - First public release. API may evolve.

## License

MIT