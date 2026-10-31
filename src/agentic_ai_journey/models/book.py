from dataclasses import dataclass
from datetime import date


@dataclass
class Book:
    title: str
    author: str
    year: int
    is_available: bool = True

    @property
    def age(self) -> int:
        """Calculate the age of the book based on the current year."""
        current_year = date.today().year
        return current_year - self.year