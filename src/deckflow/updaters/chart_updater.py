from typing import Any

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
                clean_values = [v if v is not None else 0 for v in values]
                chart_data.add_series(name, clean_values)
            self.chart.replace_data(chart_data)
            return True
        except Exception as e:
            print(f"Error applying chart data: {e}")
            return False