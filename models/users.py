"""Пользователи сервиса: организаторы и участники."""

from typing import List, Optional


class User:
    """Пользователь сервиса мероприятий."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        """Создать объект пользователя."""
        self.id = user_id
        self.name = name
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из словаря с данными JSON."""
        return cls(data["id"], data["name"], data["email"])

    def __str__(self) -> str:
        """Вернуть строковое представление пользователя."""
        return f"[{self.id}] {self.name} <{self.email}>"


def add_user(users: List[User], name: str, email: str) -> None:
    """Создать пользователя и добавить его в коллекцию."""
    new_id = max((user.id for user in users), default=0) + 1
    users.append(User(new_id, name, email))


def find_user(users: List[User], query: str) -> List[User]:
    """Найти пользователей по имени или e-mail."""
    query = query.lower()
    return [
        user for user in users
        if query in user.name.lower() or query in user.email.lower()
    ]


def find_user_by_id(users: List[User], user_id: int) -> Optional[User]:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def show_users(users: List[User]) -> None:
    """Вывести список пользователей в консоль."""
    for user in users:
        print(user)
