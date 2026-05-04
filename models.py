"""Модели данных для кинотеки."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Movie:
    """Класс, представляющий фильм."""
    
    title: str
    genre: str
    year: int
    rating: float
    
    def __post_init__(self):
        """Валидация полей после инициализации."""
        self.year = int(self.year)
        self.rating = float(self.rating)
    
    def to_dict(self) -> dict:
        """Преобразование в словарь для JSON."""
        return {
            'title': self.title,
            'genre': self.genre,
            'year': self.year,
            'rating': self.rating
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Movie':
        """Создание объекта из словаря."""
        return cls(
            title=data['title'],
            genre=data['genre'],
            year=int(data['year']),
            rating=float(data['rating'])
        )
    
    def __str__(self) -> str:
        return f"{self.title} ({self.year}) - {self.genre} - Рейтинг: {self.rating}"
