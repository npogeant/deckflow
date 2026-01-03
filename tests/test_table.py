"""Tests for table elements."""

from deckflow.elements.table import DeckTable


class FakeCell:
    """Fake cell for tests."""
    def __init__(self, text: str):
        self.text = text


class FakeRow:
    """Fake row for tests."""
    def __init__(self, cells):
        self.cells = [FakeCell(c) for c in cells]


class FakeColumn:
    """Fake column for tests."""
    def __init__(self):
        pass


class FakeTable:
    """Fake table for tests."""
    def __init__(self, data):
        self.rows = [FakeRow(row) for row in data]
        self.columns = [FakeColumn() for _ in range(len(data[0]) if data else 0)]


def test_table_initialization():
    """Verify that DeckTable initializes correctly."""
    fake_table = FakeTable([['A', 'B'], ['1', '2']])
    table = DeckTable(fake_table, "Table 1")
    
    assert table.name == "Table 1"
    assert table.rows == 2
    assert table.cols == 2
    assert table.data == [['A', 'B'], ['1', '2']]


def test_get_data():
    """Verify that we can retrieve table data."""
    fake_table = FakeTable([['A', 'B'], ['1', '2']])
    table = DeckTable(fake_table, "Table 1")
    
    data = table.get_data()
    assert data == [['A', 'B'], ['1', '2']]
    # Verify it's a copy, not the original reference
    data[0][0] = 'Z'
    assert table.data[0][0] == 'A'


def test_get_cell():
    """Verify that we can retrieve a cell."""
    fake_table = FakeTable([['A', 'B'], ['1', '2']])
    table = DeckTable(fake_table, "Table 1")
    
    assert table.get_cell(0, 0) == 'A'
    assert table.get_cell(0, 1) == 'B'
    assert table.get_cell(1, 0) == '1'
    assert table.get_cell(1, 1) == '2'


def test_get_cell_invalid():
    """Verify that we return None for an invalid cell."""
    fake_table = FakeTable([['A', 'B'], ['1', '2']])
    table = DeckTable(fake_table, "Table 1")
    
    assert table.get_cell(5, 5) is None
    assert table.get_cell(-1, 0) is None


def test_get_row():
    """Verify that we can retrieve a row."""
    fake_table = FakeTable([['A', 'B'], ['1', '2']])
    table = DeckTable(fake_table, "Table 1")
    
    row = table.get_row(0)
    assert row == ['A', 'B']
    
    row = table.get_row(1)
    assert row == ['1', '2']


def test_get_row_invalid():
    """Verify that we return None for an invalid row."""
    fake_table = FakeTable([['A', 'B'], ['1', '2']])
    table = DeckTable(fake_table, "Table 1")
    
    assert table.get_row(5) is None
    assert table.get_row(-1) is None


def test_get_column():
    """Verify that we can retrieve a column."""
    fake_table = FakeTable([['A', 'B'], ['1', '2']])
    table = DeckTable(fake_table, "Table 1")
    
    col = table.get_column(0)
    assert col == ['A', '1']
    
    col = table.get_column(1)
    assert col == ['B', '2']


def test_get_column_invalid():
    """Verify that we return None for an invalid column."""
    fake_table = FakeTable([['A', 'B'], ['1', '2']])
    table = DeckTable(fake_table, "Table 1")
    
    assert table.get_column(5) is None
    assert table.get_column(-1) is None


def test_table_dimensions():
    """Verify that dimensions are correct."""
    fake_table = FakeTable([['A', 'B', 'C'], ['1', '2', '3'], ['X', 'Y', 'Z']])
    table = DeckTable(fake_table, "Table 1")
    
    assert table.rows == 3
    assert table.cols == 3
