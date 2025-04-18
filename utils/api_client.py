import requests


class APIClient:
    BASE_URL = 'https://stellarburgers.nomoreparties.site/api'

    def __init__(self, token=None):
        self.headers = {}
        if token:
            self.headers["Authorization"] = token

    def register_user(self, data):
        return requests.post(f"{self.BASE_URL}/auth/register", json=data)

    def login_user(self, data):
        return requests.post(f"{self.BASE_URL}/auth/login", json=data)

    def delete_user(self):
        return requests.delete(f"{self.BASE_URL}/auth/user", headers=self.headers)

    def get_user(self):
        return requests.get(f"{self.BASE_URL}/auth/user", headers=self.headers)

    def update_user(self, data):
        return requests.patch(f"{self.BASE_URL}/auth/user", headers=self.headers, json=data)

    def get_ingredients(self):
        return requests.get(f"{self.BASE_URL}/ingredients")

    def create_order(self, data):
        return requests.post(f"{self.BASE_URL}/orders", headers=self.headers, json=data)

    def get_user_orders(self):
        return requests.get(f"{self.BASE_URL}/orders", headers=self.headers)

    def get_all_orders(self):
        return requests.get(f"{self.BASE_URL}/orders/all")
