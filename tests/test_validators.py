"""Тесты для валидаторов."""

import unittest
from validators import validate_movie_data, ValidationError


class TestValidators(unittest.TestCase):
    """Тесты для функций валидации."""
    
    def test_valid_data(self):
        """Позитивный тест: корректные данные."""
        result = validate_movie_data("Фильм", "Комедия", "2021", "8.0")
        self.assertEqual(result, ("Фильм", "Комедия", 2021, 8.0))
    
    def test_negative_rating(self):
        """Негативный тест: отрицательный рейтинг."""
        with self.assertRaises(ValidationError):
            validate_movie_data("Фильм", "Жанр", "2020", "-1")
    
    def test_rating_above_10(self):
        """Граничный тест: рейтинг выше 10."""
        with self.assertRaises(ValidationError):
            validate_movie_data("Фильм", "Жанр", "2020", "11")
    
    def test_rating_at_boundaries(self):
        """Граничный тест: рейтинг на границах."""
        # Нижняя граница
        result = validate_movie_data("Фильм", "Жанр", "2020", "0")
        self.assertEqual(result[3], 0.0)
        
        # Верхняя граница
        result = validate_movie_data("Фильм", "Жанр", "2020", "10")
        self.assertEqual(result[3], 10.0)
    
    def test_empty_title(self):
        """Негативный тест: пустое название."""
        with self.assertRaises(ValidationError):
            validate_movie_data("", "Жанр", "2020", "5.0")
    
    def test_invalid_year(self):
        """Негативный тест: неверный год."""
        with self.assertRaises(ValidationError):
            validate_movie_data("Фильм", "Жанр", "abc", "5.0")
    
    def test_year_at_boundaries(self):
        """Граничный тест: год на границах."""
        # Нижняя граница
        result = validate_movie_data("Фильм", "Жанр", "1888", "5.0")
        self.assertEqual(result[2], 1888)
        
        # Верхняя граница (текущий год)
        result = validate_movie_data("Фильм", "Жанр", "2026", "5.0")
        self.assertEqual(result[2], 2026)
    
    def test_year_below_min(self):
        """Граничный тест: год меньше минимального."""
        with self.assertRaises(ValidationError):
            validate_movie_data("Фильм", "Жанр", "1887", "5.0")
    
    def test_year_above_max(self):
        """Граничный тест: год больше максимального."""
        with self.assertRaises(ValidationError):
            validate_movie_data("Фильм", "Жанр", "2027", "5.0")


if __name__ == '__main__':
    unittest.main()
