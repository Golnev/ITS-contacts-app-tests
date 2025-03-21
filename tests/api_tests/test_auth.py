"""
This module contains API tests for user authentication and login functionality.
"""

import logging as logger
import pytest

from src.helpers.users_helper import UsersHelper
from src.requests_utilities import RequestUtilities

pytestmark = pytest.mark.api


@pytest.mark.auth
def test_login_and_logout(auth_headers):
    """
    Test the login and logout process for a new user.
    """

    logger.info("TEST: login and logout with new user.")
    users_helper = UsersHelper()
    user_rs_api, user_info = users_helper.create_user(auth_headers)

    request_utility = RequestUtilities()

    logger.info("Login with user email: %s", user_info["email"])

    rs_login_json = request_utility.post(
        endpoint="users/login",
        payload={
            "email": user_info["email"],
            "password": user_info["password"],
        },
    )

    assert (
        rs_login_json is not None
    ), "Response is None but expected JSON response"
    assert (
        user_rs_api is not None
    ), "Response is None but expected JSON response"
    assert (
        rs_login_json["user"]["_id"] == user_rs_api["user"]["_id"]
    ), "The IDs of the new user and the registered user do not match."

    logger.info("Logout with new user")
    rs_logout = request_utility.post(
        endpoint="users/logout",
        headers={"Authorization": f"Bearer {user_rs_api['token']}"},
    )

    assert not rs_logout, "Request is not empty."

    logger.info("Deleting a new user")
    rs_login_json = request_utility.post(
        endpoint="users/login",
        payload={
            "email": user_info["email"],
            "password": user_info["password"],
        },
    )

    assert (
        rs_login_json is not None
    ), "Response is None but expected JSON response"
    users_helper.delete_user(
        auth_headers={"Authorization": f"Bearer {rs_login_json['token']}"}
    )


@pytest.mark.auth
@pytest.mark.negative
@pytest.mark.parametrize(
    "wr_email, wr_password",
    [
        ("wrong_email_1@ex.com", "wrong_pass_1"),
        ("", "wrong_pass_2"),
        ("wrong_email_3@ex.com", ""),
    ],
)
def test_login_with_wrong_email_or_pass(wr_email: str, wr_password: str):
    """
    Test login with invalid email or password (negative test case).
    """

    logger.info("TEST: login with wrong email or pass.")

    request_utility = RequestUtilities()

    request_utility.post(
        endpoint="users/login",
        payload={"email": wr_email, "password": wr_password},
        expected_status_code=401,
    )
