import pytest


class TestLogin:

    def test_login_with_valid_credentials(self, api_client, user_data, ensure_user_created):
        """Тест для успешной авторизации с правильными данными пользователя"""
        res = api_client.login_user(user_data)
        body = res.json()

        assert res.status_code == 200
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body

    def test_login_with_invalid_credentials(self, api_client):
        """Тест для авторизации с неверными данными пользователя"""
        invalid_user_data = {
            "email": "wrong_email@yandex.ru",
            "password": "wrong_password"
        }
        res = api_client.login_user(invalid_user_data)
        body = res.json()

        assert res.status_code == 401
        assert body["success"] is False
        assert body["message"] == "email or password are incorrect"

    def test_login_with_missing_email(self, api_client):
        """Тест для авторизации без email"""
        user_data_missing_email = {
            "password": "password123"
        }
        res = api_client.login_user(user_data_missing_email)
        body = res.json()

        assert res.status_code == 401
        assert body["success"] is False
        assert body["message"] == "email or password are incorrect"

    def test_login_with_missing_password(self, api_client, user_data):
        """Тест для авторизации без пароля"""
        user_data_missing_password = {
            "email": user_data["email"]
        }
        res = api_client.login_user(user_data_missing_password)
        body = res.json()

        assert res.status_code == 401
        assert body["success"] is False
        assert body["message"] == "email or password are incorrect"
