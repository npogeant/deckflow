"""Tests for text elements."""

from deckflow.elements.text import DeckText


class FakeShape:
    """Fake shape object for tests."""
    def __init__(self, text: str):
        self.text = text
        self.has_text_frame = False
        self.name = "FakeShape"


def test_text_initialization():
    """Verify that DeckText initializes correctly."""
    shape = FakeShape("Hello World")
    text = DeckText(shape, "TextBox 1")
    
    assert text.name == "TextBox 1"
    assert text.original_content == "Hello World"
    assert text.current_content == "Hello World"


def test_get_content():
    """Verify that we can retrieve the content."""
    shape = FakeShape("Test Content")
    text = DeckText(shape, "TextBox 1")
    
    assert text.get_content() == "Test Content"


def test_get_original_content():
    """Verify that we can retrieve the original content."""
    shape = FakeShape("Original")
    text = DeckText(shape, "TextBox 1")
    text.current_content = "Modified"
    
    assert text.get_original_content() == "Original"
    assert text.get_content() == "Modified"


def test_update_text():
    """Verify that we can update the text."""
    shape = FakeShape("Old Text")
    text = DeckText(shape, "TextBox 1")
    
    text.update("New Text")
    assert text.current_content == "New Text"
    assert text.original_content == "Old Text"
