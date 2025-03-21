"""
This module contains API tests for managing users.
"""

import logging as logger
import pytest

from src.helpers.users_helper import UsersHelper
from src.requests_utilities import RequestUtilities, RequestParams

pytestmark = pytest.mark.api


@pytest.mark.users
def test_add_user():
    """
    Test adding a new user.
    """

    logger.info("TEST: Add new user.")
    users_helper = UsersHelper()
    user_rs_api, _ = users_helper.create_user()
    assert (
        user_rs_api is not None
    ), "Response is None, but expected JSON response."

    get_info_user = users_helper.get_user(
        auth_extra={"Authorization": f'Bearer {user_rs_api["token"]}'}
    )

    assert (
        get_info_user is not None
    ), "Response is None, but expected JSON response."

    assert (
        user_rs_api["user"]["_id"] == get_info_user["_id"]
    ), "User Id does not match."

    users_helper.delete_user(
        auth_extra={"Authorization": f'Bearer {user_rs_api["token"]}'}
    )


@pytest.mark.users
@pytest.mark.negative
@pytest.mark.parametrize(
    "first_name, last_name, email, password",
    [
        ("user1", "user1", "eamil1@ex.com", ""),
        ("user2", "user2", "", "password2"),
        ("user3", "user3", "", ""),
    ],
)
def test_add_user_without_email_or_password(
    first_name: str, last_name: str, email: str, password: str
):
    """
    Test adding a new user with missing email or password
    (negative test case).
    """

    logger.info("TEST: Add new user.")
    request_utility = RequestUtilities()

    payload = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "password": password,
    }

    request_params = RequestParams(
        endpoint="users", payload=payload, expected_status_code=400
    )
    rs_api = request_utility.post(request_params=request_params)

    assert rs_api is not None, "Response is None, but expected JSON response."
    assert rs_api["_message"] == "User validation failed", (
        f"User added without mandatory data."
        f"Email: {email}, "
        f"Password: {password}."
    )


@pytest.mark.users
def test_get_user_profile():
    """
    Test retrieving a user's profile.
    """

    logger.info("TEST: Get user profile.")

    users_helper = UsersHelper()

    get_info_user = users_helper.get_user()

    assert get_info_user, "Response is empty."


@pytest.mark.users
def test_update_user():
    """
    Test updating user details.
    """

    logger.info("TEST: Update user.")

    users_helper = UsersHelper()
    user_rs_api, user_info = users_helper.create_user()

    assert (
        user_rs_api is not None
    ), "Response is None, but expected JSON response."

    update_user_rs_api, update_user_info = users_helper.update_user(
        auth_extra={"Authorization": f'Bearer {user_rs_api["token"]}'}
    )

    assert (
        update_user_rs_api is not None
    ), "Response is None, but expected JSON response."

    assert user_rs_api["user"]["_id"] == update_user_rs_api["_id"], (
        f"User id does not match, "
        f"before update: {user_rs_api['user']['_id']}, "
        f"after update: {update_user_rs_api['_id']}"
    )

    assert (
        user_info["firstName"] != update_user_info["firstName"]
    ), "The first name is the same after the update"

    assert (
        user_info["lastName"] != update_user_info["lastName"]
    ), "The last name is the same after the update"

    assert (
        user_info["email"] != update_user_info["email"]
    ), "The email is the same after the update"

    assert (
        user_info["password"] != update_user_info["password"]
    ), "The password is the same after the update"

    users_helper.delete_user(
        auth_extra={"Authorization": f'Bearer {user_rs_api["token"]}'}
    )


@pytest.mark.users
@pytest.mark.negative
@pytest.mark.parametrize(
    "first_name, last_name, email, password",
    [
        ("user1", "user1", "user1@ex.com", ""),
        ("user2", "user2", "", "password2"),
        ("user3", "user3", "", ""),
    ],
)
def test_update_user_without_email_or_password(
    first_name: str, last_name: str, email: str, password: str
):
    """
    Test updating a user with missing email or password
    (negative test case).
    """

    logger.info("TEST: Update user without email or password")

    users_helper = UsersHelper()
    user_rs_api, _ = users_helper.create_user()

    assert (
        user_rs_api is not None
    ), "Response is None, but expected JSON response."

    request_utility = RequestUtilities()

    payload = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "password": password,
    }

    request_params = RequestParams(
        endpoint="users/me",
        payload=payload,
        auth_extra={"Authorization": f'Bearer {user_rs_api["token"]}'},
        expected_status_code=400,
    )
    rs_api = request_utility.patch(request_params=request_params)

    assert rs_api is not None, "Response is None, but expected JSON response."

    assert rs_api["_message"] == "User validation failed", (
        f"User updated without mandatory data."
        f"Email: {email}, "
        f"Password: {password}."
    )


@pytest.mark.users
def test_delete_new_user():
    """
    Test deleting a new user.
    """

    logger.info("TEST: Delete new user.")
    users_helper = UsersHelper()
    user_rs_api, _ = users_helper.create_user()

    assert (
        user_rs_api is not None
    ), "Response is None, but expected JSON response."

    users_helper.get_user(
        auth_extra={"Authorization": f'Bearer {user_rs_api["token"]}'}
    )

    users_helper.delete_user(
        auth_extra={"Authorization": f'Bearer {user_rs_api["token"]}'}
    )
