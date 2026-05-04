"""Модуль валидации ввода."""

from typing import Tuple


class ValidationError(Exception):
    """Пользовательское исключение для ошибок валидации."""
    pass


def validate_movie_data(title: str, genre: str, year: str, rating: str) -> Tuple[str, str, int, float]:
    """
    Валидация данных фильма.
    
    Args:
        title: Название фильма
        genre: Жанр
        year: Год выпуска (строка)
        rating: Рейтинг (строка)
    
    Returns:
        Кортеж (title, genre, year, rating) с корректными типами
    
    Raises:
        ValidationError: Если данные не прошли валидацию
    """
    errors = []
    
    # Проверка названия
    if not title or not title.strip():
        errors.append("Название фильма не может быть пустым")
    
    # Проверка жанра
    if not genre or not genre.strip():
        errors.append("Жанр не может быть пустым")
    
    # Проверка года
    try:
        year_int = int(year)
        current_year = 2026
        if year_int < 1888 or year_int > current_year:
            errors.append(f"Год должен быть от 1888 до {current_year}")
    except ValueError:
        errors.append("Год должен быть целым числом")
        year_int = 0
    
    # Проверка рейтинга
    try:
        rating_float = float(rating)
        if rating_float < 0 or rating_float > 10:
            errors.append("Рейтинг должен быть от 0 до 10")
    except ValueError:
        errors.append("Рейтинг должен быть числом от 0 до 10")
        rating_float = 0.0
    
    if errors:
        raise ValidationError("\n".join(errors))
    
    return title.strip(), genre.strip(), year_int, rating_float
