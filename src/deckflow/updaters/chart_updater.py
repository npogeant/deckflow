import logging
from typing import Any

logger = logging.getLogger(__name__)

class ChartUpdater:
    """Updater for chart elements, preserving formatting/colors."""

    def __init__(self, chart: Any):
        """
        chart: DeckChart instance
        """
        self.chart = chart

    def apply(self, data: dict) -> bool:
        try:
            from pptx.chart.data import CategoryChartData
            chart_data = CategoryChartData()
            chart_data.categories = data['categories']
            for name, values in data['series'].items():
                clean_values = [v for v in values]
                chart_data.add_series(name, clean_values)
            self.chart.replace_data(chart_data)
            return True
        except Exception:
            logger.exception("Error applying chart data")
            return False