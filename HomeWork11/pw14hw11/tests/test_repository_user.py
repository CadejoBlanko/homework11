import unittest
from unittest.mock import MagicMock
from unittest import IsolatedAsyncioTestCase

from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserModel
from ..repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
)


class TestUserFunctions(IsolatedAsyncioTestCase):

    async def test_get_user_by_email(self):
        db_session = MagicMock(spec=Session)

        test_user = User(email="test@example.com")
        db_session.query.return_value.filter.return_value.first.return_value = test_user

        result = await get_user_by_email("test@example.com", db_session)
        self.assertEqual(result, test_user)

    async def test_create_user(self):
        db_session = MagicMock(spec=Session)

        user_data = UserModel(username="test_user", email="test@example.com", password="password123")

        created_user = User(id=None, username=user_data.username, email=user_data.email, password=user_data.password)
        db_session.add.return_value = None
        db_session.commit.return_value = None
        db_session.refresh.return_value = None

        with unittest.mock.patch('libgravatar.Gravatar.get_image', return_value=None):
            result = await create_user(user_data, db_session)

        self.assertEqual(result.username, created_user.username)
        self.assertEqual(result.email, created_user.email)
        self.assertEqual(result.password, created_user.password)


    async def test_update_token(self):
        db_session = MagicMock(spec=Session)

        test_user = User(email="test@example.com")
        db_session.commit.return_value = None

        await update_token(test_user, "new_token", db_session)

        self.assertEqual(test_user.refresh_token, "new_token")

    async def test_confirmed_email(self):
        db_session = MagicMock(spec=Session)

        test_user = User(email="test@example.com")
        db_session.query.return_value.filter.return_value.first.return_value = test_user
        db_session.commit.return_value = None

        await confirmed_email("test@example.com", db_session)

        self.assertTrue(test_user.confirmed)


if __name__ == '__main__':
    unittest.main()