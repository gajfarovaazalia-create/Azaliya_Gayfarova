"""Графический интерфейс приложения."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional
from models import Movie
from validators import validate_movie_data, ValidationError
from data_manager import DataManager


class MovieLibraryApp:
    """Основной класс приложения."""
    
    def __init__(self, root: tk.Tk):
        """
        Инициализация приложения.
        
        Args:
            root: Корневой объект Tkinter
        """
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("900x600")
        
        # Менеджер данных
        self.data_manager = DataManager()
        
        # Список фильмов
        self.movies: List[Movie] = []
        
        # Создание интерфейса
        self.setup_ui()
        
        # Загрузка данных
        self.load_data()
        self.update_movie_list()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса."""
        # Главный контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка grid для main_frame
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Фрейм ввода данных
        input_frame = ttk.LabelFrame(main_frame, text="Добавление фильма", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Поля ввода
        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.genre_entry = ttk.Entry(input_frame, width=20)
        self.genre_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Label(input_frame, text="Год выпуска:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.year_entry = ttk.Entry(input_frame, width=10)
        self.year_entry.grid(row=0, column=5, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Label(input_frame, text="Рейтинг (0-10):").grid(row=0, column=6, sticky=tk.W, padx=(0, 5))
        self.rating_entry = ttk.Entry(input_frame, width=10)
        self.rating_entry.grid(row=0, column=7, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Кнопка добавления
        self.add_button = ttk.Button(input_frame, text="Добавить фильм", command=self.add_movie)
        self.add_button.grid(row=0, column=8, padx=(10, 0))
        
        # Настройка колонок для input_frame
        for i in range(9):
            input_frame.columnconfigure(i, weight=1 if i % 2 == 1 else 0)
        
        # Фрейм фильтрации
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация", padding="10")
        filter_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.filter_genre_entry = ttk.Entry(filter_frame, width=20)
        self.filter_genre_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Label(filter_frame, text="Фильтр по году:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.filter_year_entry = ttk.Entry(filter_frame, width=10)
        self.filter_year_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Кнопки фильтрации
        self.filter_button = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        self.filter_button.grid(row=0, column=4, padx=(10, 5))
        
        self.clear_filter_button = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.clear_filter)
        self.clear_filter_button.grid(row=0, column=5)
        
        # Настройка колонок для filter_frame
        for i in range(6):
            filter_frame.columnconfigure(i, weight=1)
        
        # Таблица фильмов
        table_frame = ttk.LabelFrame(main_frame, text="Список фильмов", padding="10")
        table_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Treeview для отображения фильмов
        columns = ('title', 'genre', 'year', 'rating')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Определение заголовков
        self.tree.heading('title', text='Название')
        self.tree.heading('genre', text='Жанр')
        self.tree.heading('year', text='Год')
        self.tree.heading('rating', text='Рейтинг')
        
        # Настройка ширины колонок
        self.tree.column('title', width=300)
        self.tree.column('genre', width=200)
        self.tree.column('year', width=100)
        self.tree.column('rating', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещение
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        self.save_button = ttk.Button(button_frame, text="Сохранить", command=self.save_data)
        self.save_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.delete_button = ttk.Button(button_frame, text="Удалить выбранный", command=self.delete_selected)
        self.delete_button.pack(side=tk.LEFT)
    
    def add_movie(self):
        """Добавление нового фильма."""
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()
        rating = self.rating_entry.get()
        
        try:
            validated_data = validate_movie_data(title, genre, year, rating)
            movie = Movie(*validated_data)
            self.movies.append(movie)
            
            # Очистка полей
            self.title_entry.delete(0, tk.END)
            self.genre_entry.delete(0, tk.END)
            self.year_entry.delete(0, tk.END)
            self.rating_entry.delete(0, tk.END)
            
            self.update_movie_list()
            self.save_data()
            messagebox.showinfo("Успех", f"Фильм '{movie.title}' добавлен!")
            
        except ValidationError as e:
            messagebox.showerror("Ошибка валидации", str(e))
    
    def apply_filter(self):
        """Применение фильтрации."""
        genre_filter = self.filter_genre_entry.get().strip().lower()
        year_filter = self.filter_year_entry.get().strip()
        
        filtered_movies = self.movies.copy()
        
        # Фильтр по жанру
        if genre_filter:
            filtered_movies = [m for m in filtered_movies if genre_filter in m.genre.lower()]
        
        # Фильтр по году
        if year_filter:
            try:
                year = int(year_filter)
                filtered_movies = [m for m in filtered_movies if m.year == year]
            except ValueError:
                messagebox.showwarning("Предупреждение", "Год в фильтре должен быть числом")
                return
        
        self.update_movie_list(filtered_movies)
    
    def clear_filter(self):
        """Сброс фильтрации."""
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_year_entry.delete(0, tk.END)
        self.update_movie_list()
    
    def delete_selected(self):
        """Удаление выбранного фильма."""
        selected_item = self.tree.selection()
        if selected_item:
            # Получение индекса выбранного элемента
            values = self.tree.item(selected_item)['values']
            title, genre, year, rating = values
            
            # Поиск и удаление фильма из списка
            for i, movie in enumerate(self.movies):
                if (movie.title == title and movie.genre == genre and 
                    movie.year == int(year) and movie.rating == float(rating)):
                    del self.movies[i]
                    break
            
            self.update_movie_list()
            self.save_data()
            messagebox.showinfo("Успех", f"Фильм '{title}' удален!")
    
    def update_movie_list(self, movies: Optional[List[Movie]] = None):
        """
        Обновление отображения списка фильмов.
        
        Args:
            movies: Список фильмов для отображения (если None, показываются все фильмы)
        """
        # Очистка текущего отображения
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Используем все фильмы, если не указан конкретный список
        display_movies = movies if movies is not None else self.movies
        
        # Добавление фильмов в таблицу
        for movie in display_movies:
            self.tree.insert('', tk.END, values=(
                movie.title,
                movie.genre,
                movie.year,
                movie.rating
            ))
    
    def save_data(self):
        """Сохранение данных в файл."""
        if self.data_manager.save_movies(self.movies):
            print("Данные сохранены успешно")
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить данные")
    
    def load_data(self):
        """Загрузка данных из файла."""
        self.movies = self.data_manager.load_movies()
