"""Tests for ContentRegistry."""

from deckflow.content.registry import ContentRegistry


def make_item(name: str, obj_key: str, obj):
    """Helper to create a fake item with the expected structure."""
    return {'name': name, obj_key: obj, 'is_duplicated': 'no'}


def test_registry_initialization():
    """Verify that the registry initializes correctly."""
    charts = [make_item('C1', 'chart_obj', object())]
    texts = [make_item('T1', 'text_obj', object())]
    tables = [make_item('Tab1', 'table_obj', object())]
    
    reg = ContentRegistry(charts, texts, tables)
    
    assert len(reg.charts) == 1
    assert len(reg.texts) == 1
    assert len(reg.tables) == 1


def test_get_text_by_name():
    """Verify that we can retrieve a text by its name."""
    text_obj = object()
    texts = [make_item('TextBox 1', 'text_obj', text_obj)]
    reg = ContentRegistry([], texts, [])
    
    result = reg.get_text('TextBox 1')
    assert result is text_obj


def test_get_text_not_found():
    """Verify that we return None for a non-existent text."""
    texts = [make_item('TextBox 1', 'text_obj', object())]
    reg = ContentRegistry([], texts, [])
    
    result = reg.get_text('TextBox NOPE')
    assert result is None


def test_get_chart_by_name():
    """Verify that we can retrieve a chart by its name."""
    chart_obj = object()
    charts = [make_item('Chart 1', 'chart_obj', chart_obj)]
    reg = ContentRegistry(charts, [], [])
    
    result = reg.get_chart('Chart 1')
    assert result is chart_obj


def test_get_table_by_name():
    """Verify that we can retrieve a table by its name."""
    table_obj = object()
    tables = [make_item('Table 1', 'table_obj', table_obj)]
    reg = ContentRegistry([], [], tables)
    
    result = reg.get_table('Table 1')
    assert result is table_obj


def test_count_duplicates():
    """Verify duplicate counting."""
    texts = [
        {'name': 'T1', 'text_obj': object(), 'is_duplicated': 'yes'},
        {'name': 'T2', 'text_obj': object(), 'is_duplicated': 'no'},
        {'name': 'T1', 'text_obj': object(), 'is_duplicated': 'yes'},
    ]
    reg = ContentRegistry([], texts, [])
    
    count = reg.count_duplicates('texts')
    assert count == 2
