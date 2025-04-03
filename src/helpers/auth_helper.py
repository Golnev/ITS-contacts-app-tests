"""
Authentication and Authorization Management Module.
"""

import os
from functools import wraps

import logging as logger
import requests
from src.hosts_config import API_HOSTS


class AuthManager:
    """
    Manages authentication for API requests,
    including login, logout, and token handling.
    """

    def __init__(self):
        """
        Initializes the AuthManager with the specified environment.
        """

        self.env = os.getenv("ENV")
        self.base_url = API_HOSTS[self.env]
        self.token = None

    def login(self, email=None, password=None):
        """
        Logs in to the API and retrieves an authentication token.
        """

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
            raise requests.HTTPError(
                f"Login failed with status: {response.status_code}",
                response=response,
            )

        self.token = response.json()["token"]

        logger.info("Login successful. Token: %s", self.token)
        return self.token

    def logout(self):
        """
        Logs out of the API and invalidates the current token.
        """

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
            raise requests.HTTPError(
                f"Logout failed with status: {response.status_code}",
                response=response,
            )

        logger.info("Logout successful.")
        self.token = None


def with_auth_headers(func):
    """
    A decorator that automatically adds authentication headers to a function.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        auth_manager = AuthManager()

        try:
            if not auth_manager.token:
                auth_manager.login()
            headers = {"Authorization": f"Bearer {auth_manager.token}"}

            return func(self, *args, auth_headers=headers, **kwargs)
        finally:
            auth_manager.logout()

    return wrapper
