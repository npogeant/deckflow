"""Tests for element removal utility."""

from deckflow.content.element_remover import ElementRemover


class FakeParent:
    """Fake parent node that tracks removal."""
    def __init__(self):
        self.removed = False

    def remove(self, element):
        self.removed = True


def _make_shape_with_element():
    parent = FakeParent()

    class FakeElement:
        def __init__(self, parent_ref):
            self._parent = parent_ref

        def getparent(self):
            return self._parent

    class FakeShape:
        def __init__(self, element):
            self._element = element

    element = FakeElement(parent)
    shape = FakeShape(element)
    return shape, parent


def test_remove_shape_returns_true_and_removes_from_parent():
    shape, parent = _make_shape_with_element()

    result = ElementRemover.remove_shape(shape)

    assert result is True
    assert parent.removed is True
