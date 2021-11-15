from unittest import TestCase
from unittest.mock import patch

from models.user import User
from services.user_service import UserService


class TestUserService(TestCase):
    def setUp(self) -> None:
        self.db = patch("services.user_service.db").start()
        self.mock_unique = patch(
            "services.user_service.UserService._unique_email"
        ).start()
        self.user_1 = User(
            first_name="w", last_name="z", email="wz@xyz.com", password="123"
        )
        self.user_1.id = 1
        self.user_2 = User(
            first_name="x", last_name="z", email="xz@xyz.com", password="143"
        )
        self.user_2.id = 2
        self.addCleanup(patch.stopall)

    def test_list_users(self):
        self.db.session.query.return_value = [self.user_1, self.user_2]
        service = UserService()
        actual = service.list_users()
        expected = [
            {
                "id": 1,
                "first_name": "w",
                "last_name": "z",
                "email": "wz@xyz.com",
                "password": "*****",
                "roles": [],
            },
            {
                "id": 2,
                "first_name": "x",
                "last_name": "z",
                "email": "xz@xyz.com",
                "password": "*****",
                "roles": [],
            },
        ]
        assert actual == expected

    def test_add_user(self):
        service = UserService()
        actual = service.add_user(self.user_1)
        expected = {
            "id": 1,
            "first_name": "w",
            "last_name": "z",
            "email": "wz@xyz.com",
            "password": "*****",
            "roles": [],
        }
        assert actual == expected

    def test_delete_user(self):
        self.db.session.query.return_value.filter.return_value.first.return_value = (
            self.user_1
        )
        service = UserService()
        service.delete_user(user_id=1)
        self.db.session.delete.assert_called_with(self.user_1)

    def test_update_user(self):
        self.db.session.query.return_value.filter.return_value.first.return_value = (
            self.user_1
        )
        service = UserService()
        actual = service.update_user(
            1,
            first_name="q",
            last_name="w",
            password="1234",
            email="qw@xyz.com",
        )
        expected = {
            "id": 1,
            "first_name": "q",
            "last_name": "w",
            "email": "qw@xyz.com",
            "password": "*****",
            "roles": [],
        }
        assert actual == expected
