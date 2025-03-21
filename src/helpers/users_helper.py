"""
This module provides utility functions for working with users.
"""

import logging as logger
from faker import Faker

from src.requests_utilities import RequestUtilities


class UsersHelper:
    """
    Class with methods for users.
    """

    def __init__(self):
        self.request_utility = RequestUtilities()

    def create_user(self):
        """
        Method for creating new user.
        """

        logger.info("Create new user.")
        fake = Faker()
        payload = {
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "email": fake.email(),
            "password": fake.password(length=8, special_chars=False),
        }

        logger.info(
            "Fake user first name: %s, "
            "fake user last name: %s, fake user email: %s",
            payload["firstName"],
            payload["lastName"],
            payload["email"],
        )

        create_user_json = self.request_utility.post(
            endpoint="users",
            payload=payload,
            expected_status_code=201,
        )

        return create_user_json, payload

    def delete_user(self, auth_extra=None):
        """
        Method for deleting user.
        """

        logger.info("Delete user.")

        self.request_utility.delete(endpoint="users/me", auth_extra=auth_extra)

    def get_user(self, auth_extra=None):
        """
        Method for getting user.
        """

        logger.info("Get user.")

        rs_user_info = self.request_utility.get(
            endpoint="users/me",
            auth_extra=auth_extra,
        )

        return rs_user_info

    def update_user(self, auth_extra=None):
        """
        Method for updating user.
        """

        logger.info("Update user.")

        fake = Faker()
        payload = {
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "email": fake.email(),
            "password": fake.password(length=8, special_chars=False),
        }

        logger.info(
            "Fake user update first name: %s, "
            "fake user update last name: %s, "
            "fake user update email: %s",
            payload["firstName"],
            payload["lastName"],
            payload["email"],
        )

        create_user_json = self.request_utility.patch(
            endpoint="users/me",
            payload=payload,
            auth_extra=auth_extra,
        )

        return create_user_json, payload
