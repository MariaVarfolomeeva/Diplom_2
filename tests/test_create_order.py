import pytest


class TestCreateOrder:

    def test_create_order_with_ingredients_and_auth(self, api_client, user_data, ensure_user_created, ingredients):
        """Тест для создания заказа с ингредиентами и авторизацией"""
        token = api_client.login_user(user_data).json()["accessToken"]
        order_data = {
            "ingredients": [ingredients[0]["_id"], ingredients[1]["_id"]]
        }

        res = api_client.create_order(order_data, token)
        body = res.json()

        assert res.status_code == 200
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    def test_create_order_without_ingredients(self, api_client, user_data, ensure_user_created):
        """Тест для создания заказа без ингредиентов"""
        token = api_client.login_user(user_data).json()["accessToken"]
        order_data = {
            "ingredients": []
        }

        res = api_client.create_order(order_data, token)
        body = res.json()

        assert res.status_code == 400
        assert body["success"] is False
        assert body["message"] == "Ingredient ids must be provided"

    def test_create_order_with_invalid_ingredient_hash(self, api_client, user_data, ensure_user_created):
        """Тест для создания заказа с невалидным хешем ингредиента"""
        token = api_client.login_user(user_data).json()["accessToken"]
        invalid_ingredient_id = "invalid_ingredient_hash"
        order_data = {
            "ingredients": [invalid_ingredient_id]
        }

        res = api_client.create_order(order_data, token)
        body = res.json()

        assert res.status_code == 500
        assert body["success"] is False
        assert body["message"] == "Internal Server Error"

    def test_create_order_without_auth(self, api_client, ingredients):
        """Тест для создания заказа без авторизации"""
        order_data = {
            "ingredients": [ingredients[0]["_id"], ingredients[1]["_id"]]
        }

        res = api_client.create_order(order_data)
        body = res.json()

        assert res.status_code == 401
        assert body["success"] is False
        assert body["message"] == "You should be authorised"
