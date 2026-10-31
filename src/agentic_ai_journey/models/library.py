
from dataclasses import dataclass

from agentic_ai_journey.models.book import Book

@dataclass
class Library:
    books: list[Book]

    def add_book(self, book: Book) -> None:
        """Add a book to the library."""
        self.books.append(book)

    def filter_by_author(self, author: str) -> list[Book]:
        """Filter books by a specific author."""
        return [book for book in self.books if book.author == author]

    def borrow(self, title:str) -> bool:
        """Borrow a book by title. Returns True if successful, False if the book is not available."""
        for book in self.books:
            if book.title == title and book.isAvailable:
                book.isAvailable = False
                return True
        return False


    @property
    def available_count(self) -> int:
        """Count the number of available books in the library."""
        return sum(1 for book in self.books if book.isAvailable)