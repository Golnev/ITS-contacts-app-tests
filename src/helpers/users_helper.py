"""
This module provides utility functions for working with users.
"""

import logging as logger
from faker import Faker

from src.requests_utilities import RequestUtilities, RequestParams


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

        request_params = RequestParams(
            endpoint="users",
            payload=payload,
            expected_status_code=201,
        )
        create_user_json = self.request_utility.post(
            request_params=request_params
        )

        return create_user_json, payload

    def delete_user(self, auth_extra=None):
        """
        Method for deleting user.
        """

        logger.info("Delete user.")

        request_params = RequestParams(
            endpoint="users/me",
            auth_extra=auth_extra,
        )
        self.request_utility.delete(request_params=request_params)

    def get_user(self, auth_extra=None):
        """
        Method for getting user.
        """

        logger.info("Get user.")

        request_params = RequestParams(
            endpoint="users/me",
            auth_extra=auth_extra,
        )
        rs_user_info = self.request_utility.get(request_params=request_params)

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

        request_params = RequestParams(
            endpoint="users/me",
            payload=payload,
            auth_extra=auth_extra,
        )
        create_user_json = self.request_utility.patch(
            request_params=request_params
        )

        return create_user_json, payload
