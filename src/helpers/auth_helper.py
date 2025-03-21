import os
from functools import wraps

import requests
import logging as logger
from src.hosts_config import API_HOSTS


class AuthManager:
    def __init__(self, env="test"):
        self.env = env
        self.base_url = API_HOSTS[self.env]
        self.token = None

    def login(self, email=None, password=None):
        logger.info("Performing login...")

        my_email = email or os.getenv("MY_EMAIL")
        my_pass = password or os.getenv("MY_PASSWORD")

        url = self.base_url + "users/login"
        response = requests.post(
            url=url,
            json={"email": my_email, "password": my_pass},
            timeout=10,
        )

        if response.status_code != 200:
            raise Exception(
                f"Login failed with status: {response.status_code}"
            )

        self.token = response.json()["token"]

        logger.info(f"Login successful. Token: {self.token}")
        return self.token

    def logout(self):
        if not self.token:
            logger.warning("No token found. Skipping logout.")
            return

        logger.info("logout")

        url = self.base_url + "users/logout"
        response = requests.post(
            url=url,
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=10,
        )

        if response.status_code != 200:
            raise Exception(
                f"Logout failed with status: {response.status_code}"
            )

        logger.info("Logout successful.")
        self.token = None

    def get_auth_headers(self):
        if not self.token:
            self.login()

        return {"Authorization": f"Bearer {self.token}"}


def with_auth_headers(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        auth_manager = AuthManager()
        headers = auth_manager.get_auth_headers()

        try:
            return func(self, *args, auth_headers=headers, **kwargs)
        finally:
            auth_manager.logout()

    return wrapper
