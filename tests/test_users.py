from models import User
from models.users import add_user, find_user, find_user_by_id


def test_user_creation():
    user = User(1, "Анна Смирнова", "anna@example.com")
    assert user.id == 1
    assert user.name == "Анна Смирнова"
    assert user.email == "anna@example.com"
    assert "anna@example.com" in str(user)


def test_user_from_data():
    data = {"id": 2, "name": "Иван Петров", "email": "ivan@example.com"}
    user = User.from_data(data)
    assert user.id == 2
    assert user.name == "Иван Петров"


def test_add_and_find_user():
    users = []
    add_user(users, "Анна Смирнова", "anna@example.com")
    add_user(users, "Иван Петров", "ivan@example.com")
    assert len(find_user(users, "ivan")) == 1
    assert find_user_by_id(users, 1).name == "Анна Смирнова"
    assert find_user_by_id(users, 5) is None
