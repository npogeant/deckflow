"""Tests for chart elements."""

from deckflow.elements.chart import DeckChart


class FakeChart:
    """Fake chart object for tests."""
    def __init__(self):
        self.chart_type = 1  # Type arbitraire
        self.plots = []
        self.series = []


def test_chart_initialization():
    """Verify that DeckChart initializes correctly."""
    fake_chart = FakeChart()
    chart = DeckChart(fake_chart, "Chart 1")
    
    assert chart.name == "Chart 1"
    assert chart.type == 1
    assert 'categories' in chart.data
    assert 'series' in chart.data


def test_get_data():
    """Verify that we can retrieve chart data."""
    fake_chart = FakeChart()
    chart = DeckChart(fake_chart, "Chart 1")
    
    data = chart.get_data()
    assert isinstance(data, dict)
    assert 'categories' in data
    assert 'series' in data


def test_update_categories():
    """Verify that we can update categories."""
    fake_chart = FakeChart()
    chart = DeckChart(fake_chart, "Chart 1")
    
    new_categories = ['Jan', 'Feb', 'Mar']
    chart.update_categories(new_categories)
    
    assert chart.data['categories'] == ['Jan', 'Feb', 'Mar']


def test_update_series():
    """Verify that we can update a series."""
    fake_chart = FakeChart()
    chart = DeckChart(fake_chart, "Chart 1")
    
    new_values = [10.0, 20.0, 30.0]
    chart.update_series('Series 1', new_values)
    
    assert 'Series 1' in chart.data['series']
    assert chart.data['series']['Series 1'] == [10.0, 20.0, 30.0]


def test_update_series_with_none_values():
    """Verify that None values are converted to 0."""
    fake_chart = FakeChart()
    chart = DeckChart(fake_chart, "Chart 1")
    
    new_values = [10.0, None, 30.0]
    chart.update_series('Series 1', new_values)
    
    assert chart.data['series']['Series 1'] == [10.0, 0, 30.0]
