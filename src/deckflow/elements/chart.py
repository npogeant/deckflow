from typing import Any, List

from copy import deepcopy
from ..content.chart_extractor import extract_chart_data
from ..updaters.chart_updater import ChartUpdater

class DeckChart:
    """Class to manage an individual PowerPoint chart."""

    def __init__(self, shape: Any, chart: Any, name: str):
        """
        Initialize with a PowerPoint chart object
        
        Args:
            chart: python-pptx Chart object
            name: Chart name extracted
        """
        self.shape = shape
        self.chart = chart
        self.name = name
        self.type = getattr(chart, "chart_type", None)
        self.data = extract_chart_data(chart)
        self._updater = ChartUpdater(chart)
    
    def get_data(self):
        return deepcopy(self.data)
    
    def update_series(self, series_name: str, new_values: List[float]):
        clean_values = [v if v is not None else 0 for v in new_values]
        self.data.setdefault('series', {})[series_name] = clean_values
        return self._updater.apply(self.data)
    
    def update_categories(self, new_categories: List[str]):
        self.data['categories'] = list(new_categories)
        return self._updater.apply(self.data)
    
    def save_changes(self):
        return self._updater.apply(self.data)