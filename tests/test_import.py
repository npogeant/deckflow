"""Test that the deckflow package imports correctly."""

def test_import_deckflow():
    """Verify that the main package imports without error."""
    import deckflow
    assert deckflow is not None


def test_import_deck():
    """Verify that the Deck class imports correctly."""
    from deckflow import Deck
    assert Deck is not None


def test_import_slide():
    """Verify that DeckSlide imports correctly."""
    from deckflow import DeckSlide
    assert DeckSlide is not None
