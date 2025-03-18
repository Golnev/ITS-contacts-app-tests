"""
This module contains UI tests for the "Register" page using Selenium WebDriver.
"""

import logging as logger

import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.pages.login_page import LoginPage
from src.pages.register_page import RegisterPage
from src.requests_utilities import RequestUtilities

pytestmark = pytest.mark.ui

base_url = RequestUtilities.get_base_url()


@pytest.mark.register
class TestRegisterPage:
    """
    Test suite for the "Register" page.
    """

    logger.info("Starting tests for register page.")

    def test_user_should_be_in_register_page(
        self, browser: webdriver.Firefox | webdriver.Chrome
    ):
        """
        Verifies that the user can navigate to the "Register" page.
        """

        logger.info("Starting Test: user should be in register page")
        link = base_url + "addUser"
        page = RegisterPage(browser=browser, url=link)
        page.open()
        page.should_be_register_page()

    def test_register_new_user(
        self, browser: webdriver.Firefox | webdriver.Chrome
    ):
        """
        Tests that a new user can register successfully.
        """

        logger.info("Starting Test: register new user.")
        link = base_url + "addUser"
        page = RegisterPage(browser=browser, url=link)
        page.open()

        fake = Faker()
        user_first_name = fake.first_name()
        user_last_name = fake.last_name()
        user_email = fake.email()
        user_password = fake.password(length=8, special_chars=False)
        logger.info(
            "Create fake user with\n"
            "first name: %s, "
            "last name: %s, "
            "email: %s, "
            "password: %s",
            user_first_name,
            user_last_name,
            user_email,
            user_password,
        )

        page.register_new_user(
            first_name=user_first_name,
            last_name=user_last_name,
            email=user_email,
            password=user_password,
        )

        WebDriverWait(browser, 10).until(
            EC.url_to_be(base_url + "contactList")
        )

        assert (
            page.browser.current_url == base_url + "contactList"
        ), f"Wrong URL after register. URL: {page.browser.current_url}"

    @pytest.mark.negative
    def test_register_new_user_with_short_password(
        self, browser: webdriver.Firefox | webdriver.Chrome
    ):
        """
        Tests that user registration fails with a short password.
        """

        logger.info("Starting Test: register new user.")
        link = base_url + "addUser"
        page = RegisterPage(browser=browser, url=link)
        page.open()

        fake = Faker()
        user_first_name = fake.first_name()
        user_last_name = fake.last_name()
        user_email = fake.email()
        user_password = fake.password(length=4, special_chars=False)
        logger.info(
            "Create fake user with\n"
            "first name: %s, "
            "last name: %s, "
            "email: %s, "
            "password: %s",
            user_first_name,
            user_last_name,
            user_email,
            user_password,
        )

        page.register_new_user(
            first_name=user_first_name,
            last_name=user_last_name,
            email=user_email,
            password=user_password,
        )

        page.should_be_validation_error()

    def test_cancel_from_register_page(
        self, browser: webdriver.Firefox | webdriver.Chrome
    ):
        """
        Verifies that the user can cancel registration
        and return to the "Login" page.
        """

        logger.info("Starting Test: cancel from register page.")
        link = base_url + "addUser"
        page = RegisterPage(browser=browser, url=link)
        page.open()

        page.cancel_from_register_page()

        login_page = LoginPage(browser=browser, url=browser.current_url)
        login_page.should_be_login_page()
