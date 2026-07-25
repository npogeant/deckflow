"""Tests for DeckSlide's element removal methods."""

import pytest

from deckflow.slide import DeckSlide
from deckflow.content.registry import ContentRegistry


class FakeParent:
    """Fake parent node that tracks removal."""
    def __init__(self):
        self.removed = False

    def remove(self, element):
        self.removed = True


class FakeElement:
    """Fake XML element supporting getparent()/remove()."""
    def __init__(self, parent):
        self._parent = parent

    def getparent(self):
        return self._parent


class FakeShape:
    """Fake shape that can be removed via ElementRemover."""
    def __init__(self, element):
        self._element = element


class UnremovableShape:
    """Fake shape with no _element/_sp, so removal always fails."""
    pass


class FakeItem:
    """Fake DeckText/DeckChart/DeckTable stand-in exposing a .shape."""
    def __init__(self, shape):
        self.shape = shape


def _make_slide(charts=None, texts=None, tables=None) -> DeckSlide:
    """Build a DeckSlide backed by a real ContentRegistry, skipping pptx scanning."""
    slide = DeckSlide.__new__(DeckSlide)
    slide.registry = ContentRegistry(charts or [], texts or [], tables or [])
    return slide


def _entry(name, obj_key, obj):
    return {"name": name, obj_key: obj, "is_duplicated": "no"}


def test_remove_text_removes_shape():
    parent = FakeParent()
    item = FakeItem(FakeShape(FakeElement(parent)))
    slide = _make_slide(texts=[_entry("Title", "text_obj", item)])

    assert slide.remove_text("Title") is True
    assert parent.removed is True


def test_remove_chart_removes_shape():
    parent = FakeParent()
    item = FakeItem(FakeShape(FakeElement(parent)))
    slide = _make_slide(charts=[_entry("Chart 1", "chart_obj", item)])

    assert slide.remove_chart("Chart 1") is True
    assert parent.removed is True


def test_remove_table_removes_shape():
    parent = FakeParent()
    item = FakeItem(FakeShape(FakeElement(parent)))
    slide = _make_slide(tables=[_entry("Table 1", "table_obj", item)])

    assert slide.remove_table("Table 1") is True
    assert parent.removed is True


def test_remove_text_not_found_raises_value_error():
    slide = _make_slide(texts=[])

    with pytest.raises(ValueError, match="Text element 'Missing' not found"):
        slide.remove_text("Missing")


def test_remove_chart_not_found_raises_value_error():
    slide = _make_slide(charts=[])

    with pytest.raises(ValueError, match="Chart 'Missing' not found"):
        slide.remove_chart("Missing")


def test_remove_table_not_found_raises_value_error():
    slide = _make_slide(tables=[])

    with pytest.raises(ValueError, match="Table 'Missing' not found"):
        slide.remove_table("Missing")


def test_remove_text_failure_raises_runtime_error():
    item = FakeItem(UnremovableShape())
    slide = _make_slide(texts=[_entry("Title", "text_obj", item)])

    with pytest.raises(RuntimeError, match="Failed to remove text element 'Title'"):
        slide.remove_text("Title")
