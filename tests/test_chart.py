"""Tests for chart elements."""

from deckflow.elements.chart import DeckChart


class FakeChart:
    """Fake chart object for tests."""
    def __init__(self):
        self.chart_type = 1
        self.plots = []
        self.series = []


class FakeShape:
    """Fake shape holding a chart reference."""
    def __init__(self, chart, name="Chart 1"):
        self.chart = chart
        self.name = name


def make_chart(name="Chart 1"):
    fake_chart = FakeChart()
    shape = FakeShape(fake_chart, name)
    return DeckChart(shape, fake_chart, name)


def test_chart_initialization():
    """Verify that DeckChart initializes correctly."""
    chart = make_chart("Chart 1")
    
    assert chart.name == "Chart 1"
    assert chart.type == 1
    assert 'categories' in chart.data
    assert 'series' in chart.data


def test_get_data():
    """Verify that we can retrieve chart data."""
    chart = make_chart("Chart 1")
    
    data = chart.get_data()
    assert isinstance(data, dict)
    assert 'categories' in data
    assert 'series' in data


def test_update_categories():
    """Verify that we can update categories."""
    chart = make_chart("Chart 1")
    
    new_categories = ['Jan', 'Feb', 'Mar']
    chart.update_categories(new_categories)
    
    assert chart.data['categories'] == ['Jan', 'Feb', 'Mar']


def test_update_series():
    """Verify that we can update a series."""
    chart = make_chart("Chart 1")
    
    new_values = [10.0, 20.0, 30.0]
    chart.update_series('Series 1', new_values)
    
    assert 'Series 1' in chart.data['series']
    assert chart.data['series']['Series 1'] == [10.0, 20.0, 30.0]


def test_update_series_with_none_values():
    """Verify that None values are converted to 0."""
    chart = make_chart("Chart 1")
    
    new_values = [10.0, None, 30.0]
    chart.update_series('Series 1', new_values)
    
    assert chart.data['series']['Series 1'] == [10.0, 0, 30.0]
