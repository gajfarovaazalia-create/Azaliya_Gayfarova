"""Тесты для моделей данных."""

import unittest
from models import Movie


class TestMovie(unittest.TestCase):
    """Тесты для класса Movie."""
    
    def test_create_movie(self):
        """Позитивный тест: создание фильма."""
        movie = Movie("Интерстеллар", "Фантастика", 2014, 8.6)
        self.assertEqual(movie.title, "Интерстеллар")
        self.assertEqual(movie.genre, "Фантастика")
        self.assertEqual(movie.year, 2014)
        self.assertEqual(movie.rating, 8.6)
    
    def test_movie_to_dict(self):
        """Тест: преобразование в словарь."""
        movie = Movie("Матрица", "Фантастика", 1999, 8.7)
        expected = {
            'title': 'Матрица',
            'genre': 'Фантастика',
            'year': 1999,
            'rating': 8.7
        }
        self.assertEqual(movie.to_dict(), expected)
    
    def test_movie_from_dict(self):
        """Тест: создание из словаря."""
        data = {
            'title': 'Начало',
            'genre': 'Триллер',
            'year': 2010,
            'rating': 8.8
        }
        movie = Movie.from_dict(data)
        self.assertEqual(movie.title, 'Начало')
        self.assertEqual(movie.genre, 'Триллер')
        self.assertEqual(movie.year, 2010)
        self.assertEqual(movie.rating, 8.8)
    
    def test_type_conversion(self):
        """Тест: преобразование типов."""
        movie = Movie("Фильм", "Драма", "2020", "7.5")
        self.assertIsInstance(movie.year, int)
        self.assertIsInstance(movie.rating, float)
        self.assertEqual(movie.year, 2020)
        self.assertEqual(movie.rating, 7.5)


if __name__ == '__main__':
    unittest.main()
