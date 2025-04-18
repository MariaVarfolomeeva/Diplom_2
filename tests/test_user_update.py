import pytest


class TestUserUpdate:

    def test_update_user_data_with_auth(self, api_client, user_data, ensure_user_created):
        """Тест для обновления данных пользователя с авторизацией"""
        token = api_client.login_user(user_data).json()["accessToken"]
        updated_data = {"name": "UpdatedUserName"}

        res = api_client.update_user(updated_data, token)
        body = res.json()

        assert res.status_code == 200
        assert body["success"] is True
        assert body["user"]["name"] == updated_data["name"]

    def test_update_user_data_without_auth_should_fail(self, api_client, user_data):
        """Тест для попытки обновления данных пользователя без авторизации"""
        updated_data = {"name": "UpdatedUserName"}

        res = api_client.update_user(updated_data)
        body = res.json()

        assert res.status_code == 401
        assert body["success"] is False
        assert body["message"] == "You should be authorised"

    def test_update_user_email_to_existing_email(self, api_client, user_data, ensure_user_created):
        """Тест для попытки обновления email на уже существующий"""
        token = api_client.login_user(user_data).json()["accessToken"]
        existing_email = "existing_user@yandex.ru"
        updated_data = {"email": existing_email}

        res = api_client.update_user(updated_data, token)
        body = res.json()

        assert res.status_code == 403
        assert body["success"] is False
        assert body["message"] == "User with such email already exists"

    def test_update_user_data_with_partial_data(self, api_client, user_data, ensure_user_created):
        """Тест для частичного обновления данных (например, только имени)"""
        token = api_client.login_user(user_data).json()["accessToken"]
        updated_data = {"name": "PartiallyUpdatedUser"}

        res = api_client.update_user(updated_data, token)
        body = res.json()

        assert res.status_code == 200
        assert body["success"] is True
        assert body["user"]["name"] == updated_data["name"]

    def test_update_user_data_invalid_field(self, api_client, user_data, ensure_user_created):
        """Тест для обновления данных с невалидным полем"""
        token = api_client.login_user(user_data).json()["accessToken"]
        updated_data = {"invalid_field": "SomeValue"}

        res = api_client.update_user(updated_data, token)
        body = res.json()

        assert res.status_code == 400
        assert body["success"] is False
        assert body["message"] == "Invalid field"
