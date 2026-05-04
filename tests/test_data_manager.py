"""Тесты для менеджера данных."""

import os
import unittest
from models import Movie
from data_manager import DataManager


class TestDataManager(unittest.TestCase):
    """Тесты для класса DataManager."""
    
    def setUp(self):
        """Подготовка перед тестами."""
        self.test_file = "test_movies.json"
        self.data_manager = DataManager(self.test_file)
        self.test_movies = [
            Movie("Фильм 1", "Комедия", 2020, 7.5),
            Movie("Фильм 2", "Драма", 2019, 8.0),
            Movie("Фильм 3", "Фантастика", 2021, 9.0)
        ]
    
    def tearDown(self):
        """Очистка после тестов."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_save_and_load(self):
        """Тест: сохранение и загрузка данных."""
        # Сохранение
        result = self.data_manager.save_movies(self.test_movies)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_file))
        
        # Загрузка
        loaded_movies = self.data_manager.load_movies()
        self.assertEqual(len(loaded_movies), 3)
        self.assertEqual(loaded_movies[0].title, "Фильм 1")
        self.assertEqual(loaded_movies[1].genre, "Драма")
        self.assertEqual(loaded_movies[2].year, 2021)
    
    def test_load_empty_file(self):
        """Тест: загрузка несуществующего файла."""
        movies = self.data_manager.load_movies()
        self.assertEqual(movies, [])
    
    def test_save_empty_list(self):
        """Тест: сохранение пустого списка."""
        result = self.data_manager.save_movies([])
        self.assertTrue(result)
        
        loaded = self.data_manager.load_movies()
        self.assertEqual(loaded, [])


if __name__ == '__main__':
    unittest.main()
