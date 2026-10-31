from dataclasses import dataclass


@dataclass
class Book:
    title: str
    author: str
    year: int
    isAvailable: bool = True

    @property
    def age(self) -> int:
        """Calculate the age of the book based on the current year."""
        from datetime import datetime
        current_year = datetime.now().year
        return current_year - self.year