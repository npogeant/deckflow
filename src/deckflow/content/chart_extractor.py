from typing import Any, Dict, List

def extract_chart_data(chart: Any) -> Dict[str, Any]:
    """ Extract chart data safely from a pptx chart object."""
    data: Dict[str, Any] = {'categories': [], 'series': {}}
    try:
        # Categories
        if getattr(chart, "plots", None):
            first_plot = chart.plots[0] if len(chart.plots) > 0 else None
            if first_plot and getattr(first_plot, "categories", None):
                data['categories'] = [getattr(c, "label", "") for c in first_plot.categories]
        
        # Series
        if getattr(chart, "series", None):
            for i, series in enumerate(chart.series):
                name = series.name or f"Series_{i+1}"
                values: List[Any] = [v if v is not None else 0 for v in getattr(series, "values", [])]
                # Ensure 'series' is a mapping before assigning
                if not isinstance(data.get('series'), dict):
                    data['series'] = {}
                data['series'][name] = values
    except Exception as e:
        print(f"Error extracting chart data: {e}")
    return data