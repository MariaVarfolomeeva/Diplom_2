import pytest
import requests
from utils.api_client import APIClient


@pytest.fixture(scope="session")
def api_client():
    """Фикстура для создания экземпляра APIClient"""
    return APIClient()


@pytest.fixture(scope="session")
def user_data():
    """Данные для пользователя для регистрации и авторизации"""
    return {
        "email": "testuser@example.com",
        "password": "password123",
        "name": "Test User"
    }


@pytest.fixture(scope="session")
def ensure_user_created(api_client, user_data):
    """Фикстура для регистрации пользователя"""
    response = api_client.register_user(user_data)
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope="session")
def ingredients(api_client):
    """Фикстура для получения списка ингредиентов"""
    response = api_client.get_ingredients()
    assert response.status_code == 200
    return response.json()["data"]


@pytest.fixture(scope="function")
def create_order(api_client, ingredients, user_data, ensure_user_created):
    """Фикстура для создания заказа с ингредиентами"""
    token = api_client.login_user(user_data).json()["accessToken"]
    order_data = {
        "ingredients": [ingredients[0]["_id"], ingredients[1]["_id"]]
    }
    response = api_client.create_order(order_data, token)
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope="function")
def create_multiple_orders(api_client, ingredients, user_data, ensure_user_created):
    """Фикстура для создания нескольких заказов"""
    token = api_client.login_user(user_data).json()["accessToken"]
    order_data_1 = {
        "ingredients": [ingredients[0]["_id"], ingredients[1]["_id"]]
    }
    order_data_2 = {
        "ingredients": [ingredients[1]["_id"], ingredients[2]["_id"]]
    }
    response_1 = api_client.create_order(order_data_1, token)
    response_2 = api_client.create_order(order_data_2, token)

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    return response_1.json(), response_2.json()


@pytest.fixture(scope="function")
def invalid_token():
    """Фикстура для получения невалидного токена"""
    return "invalid_token"


@pytest.fixture(scope="session")
def get_auth_token(api_client, user_data, ensure_user_created):
    """Фикстура для получения токена авторизации"""
    response = api_client.login_user(user_data)
    assert response.status_code == 200
    return response.json()["accessToken"]
