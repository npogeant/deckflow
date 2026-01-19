from typing import Any, Dict, List

from ..elements.chart import DeckChart
from ..elements.text import DeckText
from ..elements.table import DeckTable

class ContentFinder:
    """Finds and wraps all content in a slide."""
    
    def __init__(self):
        self.charts = []
        self.texts = []
        self.tables = []
        self._counters = {'chart': 0, 'text': 0, 'table': 0}
    
    def find_all(self, slide: Any) -> Dict[str, List[Any]]:
        """Find all content in the slide."""
        for i, shape in enumerate(slide.shapes):
            self._search_recursive(shape, f"shape_{i}")
        
        return {
            'charts': self.charts,
            'texts': self.texts,
            'tables': self.tables
        }

    def _search_recursive(self, shape: Any, path: str = "") -> None:
        """Recursively search through shape groups."""
        if hasattr(shape, 'shapes'):  # Group shape
            for i, sub_shape in enumerate(shape.shapes):
                self._search_recursive(sub_shape, f"{path}.group[{i}]")
        else:
            self._process_shape(shape, path)
    
    def _process_shape(self, shape: Any, path: str) -> None:
        """Process a single shape and categorize it."""
        if self._is_table(shape):
            self._add_table(shape, path)
        elif self._is_chart(shape):
            self._add_chart(shape, path)
        elif self._is_text(shape):
            self._add_text(shape, path)
    
    def _is_table(self, shape: Any) -> bool:
        return hasattr(shape, 'has_table') and shape.has_table
    
    def _is_chart(self, shape: Any) -> bool:
        return hasattr(shape, 'has_chart') and shape.has_chart
    
    def _is_text(self, shape: Any) -> bool:
        return ((hasattr(shape, 'text') and shape.text.strip()) or
                (hasattr(shape, 'has_text_frame') and shape.has_text_frame))
    
    def _add_table(self, shape: Any, path: str) -> None:
        self.tables.append({
            'name': shape.name,
            'table_obj': DeckTable(shape, shape.table, shape.name),
            'shape': shape,
            'path': path
        })
        self._counters['table'] += 1
    
    def _add_chart(self, shape, path):
        self.charts.append({
            'name': shape.name,
            'chart_obj': DeckChart(shape, shape.chart, shape.name),
            'raw_chart': shape.chart,
            'type': shape.chart.chart_type,
            'shape': shape,
            'path': path
        })
        self._counters['chart'] += 1
    
    def _add_text(self, shape, path):
        self.texts.append({
            'name': shape.name,
            'text_obj': DeckText(shape, shape.name),
            'shape': shape,
            'path': path
        })
        self._counters['text'] += 1