"""Модуль для работы с JSON-хранилищем."""

import json
import os
from typing import List
from models import Movie


class DataManager:
    """Класс для управления данными в JSON."""
    
    def __init__(self, filename: str = "movies.json"):
        """
        Инициализация менеджера данных.
        
        Args:
            filename: Имя файла для хранения данных
        """
        self.filename = filename
    
    def save_movies(self, movies: List[Movie]) -> bool:
        """
        Сохранение списка фильмов в JSON-файл.
        
        Args:
            movies: Список объектов Movie
        
        Returns:
            True если успешно, False при ошибке
        """
        try:
            movies_data = [movie.to_dict() for movie in movies]
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(movies_data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            return False
    
    def load_movies(self) -> List[Movie]:
        """
        Загрузка списка фильмов из JSON-файла.
        
        Returns:
            Список объектов Movie
        """
        if not os.path.exists(self.filename):
            return []
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                movies_data = json.load(f)
            
            movies = []
            for movie_data in movies_data:
                try:
                    movie = Movie.from_dict(movie_data)
                    movies.append(movie)
                except Exception as e:
                    print(f"Ошибка при загрузке фильма: {e}")
                    continue
            
            return movies
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
            return []
