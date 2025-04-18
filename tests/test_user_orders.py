import pytest


class TestUserOrders:

    def test_get_user_orders_with_auth(self, api_client, user_data, ensure_user_created, create_order):
        """Тест для получения заказов авторизованного пользователя"""
        token = api_client.login_user(user_data).json()["accessToken"]

        res = api_client.get_user_orders(token)
        body = res.json()

        assert res.status_code == 200
        assert body["success"] is True
        assert "orders" in body
        assert isinstance(body["orders"], list)
        assert body["total"] >= 0

    def test_get_user_orders_without_auth(self, api_client):
        """Тест для получения заказов неавторизованного пользователя"""
        res = api_client.get_user_orders()
        body = res.json()

        assert res.status_code == 401
        assert body["success"] is False
        assert body["message"] == "You should be authorised"

    def test_get_user_orders_with_no_orders(self, api_client, user_data, ensure_user_created):
        """Тест для получения заказов пользователя, у которого нет заказов"""
        token = api_client.login_user(user_data).json()["accessToken"]

        res = api_client.get_user_orders(token)
        body = res.json()

        assert res.status_code == 200
        assert body["success"] is True
        assert "orders" in body
        assert len(body["orders"]) == 0

    def test_get_user_orders_with_multiple_orders(self, api_client, user_data, ensure_user_created,
                                                  create_multiple_orders):
        """Тест для получения нескольких заказов пользователя"""
        token = api_client.login_user(user_data).json()["accessToken"]

        res = api_client.get_user_orders(token)
        body = res.json()

        assert res.status_code == 200
        assert body["success"] is True
        assert "orders" in body
        assert len(body["orders"]) > 0

    def test_get_user_orders_invalid_token(self, api_client, invalid_token):
        """Тест для получения заказов с невалидным токеном"""
        res = api_client.get_user_orders(invalid_token)
        body = res.json()

        assert res.status_code == 401
        assert body["success"] is False
        assert body["message"] == "You should be authorised"
