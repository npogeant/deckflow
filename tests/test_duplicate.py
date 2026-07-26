"""Tests for DuplicateManager."""

from deckflow.content.duplicate import DuplicateManager


def test_mark_duplicates_flags_repeated_names():
    items = [
        {'name': 'A'},
        {'name': 'B'},
        {'name': 'A'},
    ]

    DuplicateManager.mark_duplicates(items)

    assert items[0]['is_duplicated'] == 'yes'
    assert items[1]['is_duplicated'] == 'no'
    assert items[2]['is_duplicated'] == 'yes'


def test_mark_duplicates_no_repeats():
    items = [{'name': 'A'}, {'name': 'B'}]

    DuplicateManager.mark_duplicates(items)

    assert all(item['is_duplicated'] == 'no' for item in items)


def test_get_duplicates_counts_only_flagged_items():
    items = [
        {'name': 'A', 'is_duplicated': 'yes'},
        {'name': 'A', 'is_duplicated': 'yes'},
        {'name': 'B', 'is_duplicated': 'no'},
    ]

    result = DuplicateManager.get_duplicates(items)

    assert result == {'A': 2}


def test_get_duplicates_empty_when_none_flagged():
    items = [{'name': 'A', 'is_duplicated': 'no'}]

    assert DuplicateManager.get_duplicates(items) == {}


def test_has_duplicates_true_for_duplicated_name():
    items = [
        {'name': 'A', 'is_duplicated': 'yes'},
        {'name': 'A', 'is_duplicated': 'yes'},
    ]

    assert DuplicateManager.has_duplicates(items, 'A') is True


def test_has_duplicates_false_for_unique_name():
    items = [
        {'name': 'A', 'is_duplicated': 'no'},
        {'name': 'B', 'is_duplicated': 'no'},
    ]

    assert DuplicateManager.has_duplicates(items, 'A') is False


def test_has_duplicates_false_for_unknown_name():
    items = [{'name': 'A', 'is_duplicated': 'no'}]

    assert DuplicateManager.has_duplicates(items, 'NOPE') is False
