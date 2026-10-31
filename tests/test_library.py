import pytest

from agentic_ai_journey.models.book import Book
from agentic_ai_journey.models.library import Library


@pytest.fixture
def library():
    return Library(
        books=[
            Book("Dune", "Frank Herbert", 1965),
            Book("Children of Dune", "Frank Herbert", 1976),
            Book("Neuromancer", "William Gibson", 1984, isAvailable=False),
        ]
    )


def test_add_book_appends_to_library(library):
    book = Book("Foundation", "Isaac Asimov", 1951)
    library.add_book(book)
    assert library.books[-1] is book
    assert len(library.books) == 4


def test_add_book_to_empty_library():
    library = Library(books=[])
    library.add_book(Book("Foundation", "Isaac Asimov", 1951))
    assert len(library.books) == 1


def test_filter_by_author_returns_matching_books(library):
    titles = [book.title for book in library.filter_by_author("Frank Herbert")]
    assert titles == ["Dune", "Children of Dune"]


def test_filter_by_author_returns_empty_list_for_unknown_author(library):
    assert library.filter_by_author("Unknown") == []


def test_filter_by_author_is_case_sensitive(library):
    assert library.filter_by_author("frank herbert") == []


def test_borrow_available_book_succeeds(library):
    assert library.borrow("Dune") is True
    assert library.books[0].isAvailable is False


def test_borrow_same_book_twice_fails(library):
    assert library.borrow("Dune") is True
    assert library.borrow("Dune") is False


def test_borrow_unavailable_book_fails(library):
    assert library.borrow("Neuromancer") is False


def test_borrow_missing_book_fails(library):
    assert library.borrow("Missing Title") is False


def test_available_count(library):
    assert library.available_count == 2


def test_available_count_decreases_after_borrow(library):
    library.borrow("Dune")
    assert library.available_count == 1


def test_available_count_increases_after_adding_book(library):
    library.add_book(Book("Foundation", "Isaac Asimov", 1951))
    assert library.available_count == 3


def test_available_count_empty_library():
    assert Library(books=[]).available_count == 0
