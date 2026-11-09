"""Вспомогательные функции консольного ввода."""

from datetime import datetime


def input_int(prompt: str) -> int:
    """Запросить целое число; при ошибке повторить запрос."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Нужно ввести целое число")


def input_date(prompt: str) -> str:
    """Запросить дату ДД.ММ.ГГГГ и вернуть её в формате ГГГГ-ММ-ДД."""
    while True:
        try:
            value = datetime.strptime(input(prompt), "%d.%m.%Y")
            return value.date().isoformat()
        except ValueError:
            print("Дата вводится в формате ДД.ММ.ГГГГ")
