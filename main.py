"""Главный модуль для запуска приложения Movie Library."""

import tkinter as tk
from gui import MovieLibraryApp


def main():
    """Точка входа в приложение."""
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
