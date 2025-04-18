import pytest


class TestRegister:

    def test_register_with_unique_user(self, api_client):
        """Тест для успешной регистрации с уникальными данными пользователя"""
        user_data = {
            "email": "new_user@yandex.ru",
            "password": "password123",
            "name": "NewUser"
        }
        res = api_client.create_user(user_data)
        body = res.json()

        assert res.status_code == 200
        assert body["success"] is True
        assert body["user"]["email"] == user_data["email"]
        assert body["user"]["name"] == user_data["name"]
        assert "accessToken" in body
        assert "refreshToken" in body

    def test_register_with_existing_user(self, api_client, user_data, ensure_user_created):
        """Тест для регистрации с уже существующим пользователем"""
        res = api_client.create_user(user_data)
        body = res.json()

        assert res.status_code == 403
        assert body["success"] is False
        assert body["message"] == "User already exists"

    def test_register_with_missing_email(self, api_client):
        """Тест для регистрации с отсутствующим email"""
        user_data_missing_email = {
            "password": "password123",
            "name": "NoEmailUser"
        }
        res = api_client.create_user(user_data_missing_email)
        body = res.json()

        assert res.status_code == 403
        assert body["success"] is False
        assert body["message"] == "Email, password and name are required fields"

    def test_register_with_missing_password(self, api_client):
        """Тест для регистрации с отсутствующим паролем"""
        user_data_missing_password = {
            "email": "no_password@yandex.ru",
            "name": "NoPasswordUser"
        }
        res = api_client.create_user(user_data_missing_password)
        body = res.json()

        assert res.status_code == 403
        assert body["success"] is False
        assert body["message"] == "Email, password and name are required fields"

    def test_register_with_missing_name(self, api_client):
        """Тест для регистрации с отсутствующим именем"""
        user_data_missing_name = {
            "email": "no_name@yandex.ru",
            "password": "password123"
        }
        res = api_client.create_user(user_data_missing_name)
        body = res.json()

        assert res.status_code == 403
        assert body["success"] is False
        assert body["message"] == "Email, password and name are required fields"
