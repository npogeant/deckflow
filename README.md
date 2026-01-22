# Deckflow

A library to manage the content of PowerPoint presentations, built on python-pptx. Deckflow enables you to extract, analyze, and modify the content of PPTX files in a simple and intuitive way.

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

### Basic usage
```python
from deckflow import Deck

# Load a presentation
deck = Deck("presentation.pptx")

# Iterate slides
for slide in deck.slides:
    print(slide)
```

### Inspect a slide
```python
slide = deck.get_slide(1)
slide.list_content() # print available texts/charts/tables on the slide
```

### Read and update text
```python
print(slide.get_text("TextName").get_content())
slide.update_text("TextName", "New Text")
```

### Work with charts
```python
chart = slide.get_chart("ChartName")
data = chart.get_data()

# update categories and series (example data)
slide.update_chart("ChartName", {
    'categories': ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep'],
    'series': {
        'Serie 1':  [182.0,190.0,209.0,220.0,227.0,231.0,524.0,236.0,249.0],
        'Serie 2': [61.0,109.0,123.0,116.0,119.0,121.0,132.0,138.0,134.0]
    }
})
```

### Update tables
```python
slide.update_table("TableName",
                   [['Product', 'Q1', 'Q2', 'Q3'], ['Widget', '100', '120', '130'], ['Gadget', '80', '95', '105']],
                   by_rows=False, by_columns=True)
```

### Save changes
```python
deck.save("updated_presentation.pptx")
```

## Project Status

⚠️ Version 0.1.4

## License

MIT