"""Tests for ContentFinder."""

from deckflow.content.finder import ContentFinder


class FakeCell:
    def __init__(self, text):
        self.text = text


class FakeRow:
    def __init__(self, cells):
        self.cells = cells


class FakeTable:
    def __init__(self, rows_data):
        self.rows = [FakeRow([FakeCell(v) for v in row]) for row in rows_data]
        self.columns = rows_data[0] if rows_data else []


class FakeTableShape:
    def __init__(self, name, rows_data):
        self.name = name
        self.has_table = True
        self.table = FakeTable(rows_data)


class FakeChart:
    def __init__(self, chart_type="BAR"):
        self.chart_type = chart_type
        self.plots = []
        self.series = []


class FakeChartShape:
    def __init__(self, name, chart_type="BAR"):
        self.name = name
        self.has_chart = True
        self.chart = FakeChart(chart_type)


class FakeTextShape:
    def __init__(self, name, text):
        self.name = name
        self.text = text


class FakeEmptyTextFrame:
    def __init__(self):
        self.paragraphs = []


class FakeTextFrameShape:
    """A shape with no direct text but a text frame (e.g. an empty placeholder)."""
    def __init__(self, name):
        self.name = name
        self.text = ""
        self.has_text_frame = True
        self.text_frame = FakeEmptyTextFrame()


class FakeUnrecognizedShape:
    """A shape that is neither a table, chart, nor text (e.g. a picture)."""
    def __init__(self, name):
        self.name = name


class FakeGroupShape:
    def __init__(self, name, shapes):
        self.name = name
        self.shapes = shapes


def test_find_all_categorizes_top_level_shapes():
    slide = FakeGroupShape("slide", [
        FakeTableShape("Table 1", [["a", "b"], ["c", "d"]]),
        FakeChartShape("Chart 1"),
        FakeTextShape("Text 1", "Hello"),
    ])

    finder = ContentFinder()
    result = finder.find_all(slide)

    assert [t['name'] for t in result['tables']] == ["Table 1"]
    assert [c['name'] for c in result['charts']] == ["Chart 1"]
    assert [t['name'] for t in result['texts']] == ["Text 1"]


def test_find_all_ignores_unrecognized_shapes():
    slide = FakeGroupShape("slide", [FakeUnrecognizedShape("Picture 1")])

    finder = ContentFinder()
    result = finder.find_all(slide)

    assert result == {'charts': [], 'texts': [], 'tables': []}


def test_find_all_recurses_into_grouped_shapes():
    inner_group = FakeGroupShape("Group 1", [
        FakeTextShape("Nested Text", "Nested"),
    ])
    slide = FakeGroupShape("slide", [inner_group])

    finder = ContentFinder()
    result = finder.find_all(slide)

    assert [t['name'] for t in result['texts']] == ["Nested Text"]
    assert result['texts'][0]['path'] == "shape_0.group[0]"


def test_find_all_detects_text_via_text_frame_when_text_is_empty():
    slide = FakeGroupShape("slide", [FakeTextFrameShape("Placeholder 1")])

    finder = ContentFinder()
    result = finder.find_all(slide)

    assert [t['name'] for t in result['texts']] == ["Placeholder 1"]


def test_find_all_populates_expected_entry_fields():
    slide = FakeGroupShape("slide", [FakeChartShape("Chart 1", chart_type="LINE")])

    finder = ContentFinder()
    result = finder.find_all(slide)

    entry = result['charts'][0]
    assert entry['type'] == "LINE"
    assert entry['raw_chart'] is slide.shapes[0].chart
    assert entry['shape'] is slide.shapes[0]
    assert entry['path'] == "shape_0"
