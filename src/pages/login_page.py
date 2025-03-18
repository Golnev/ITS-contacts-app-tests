"""
This module provides methods for interacting with the "Login" page.
"""

import logging as logger
from src.locators import LoginPageLocators
from src.pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Class for interacting with the 'Login' page.
    """

    def should_be_login_page(self):
        """
        Verify that the current page is the 'Login' page.
        """

        self.should_be_login_url()
        self.should_be_login_form()
        self.should_be_register_button()

    def should_be_login_url(self):
        """
        Verify that the URL of the current page
        matches the expected 'Login' page URL.
        """

        logger.info("Check login url")
        assert (
            self.browser.current_url == LoginPageLocators.LOGIN_PAGE_URL
        ), "URL address is not correct."

    def should_be_login_form(self):
        """
        Verify the presence of the login form on the page.
        """

        logger.info("Check login from on login page is present.")
        assert self.is_element_present(
            *LoginPageLocators.LOGIN_FORM
        ), "Login form is not presented."

    def should_be_register_button(self):
        """
        Verify the presence of the register button on the 'Login' page.
        """

        logger.info("Check login button on login page is present.")
        assert self.is_element_present(
            *LoginPageLocators.SIGN_UP_BUTTON
        ), "Sign up button is not presented."

    def go_to_register_page(self):
        """
        Navigate to the registration page from the 'Login' page.
        """

        logger.info("Go to register page")
        link = self.browser.find_element(*LoginPageLocators.SIGN_UP_BUTTON)
        link.click()

    def login(self, email: str, password: str):
        """
        Perform the login action using the provided email and password.
        """

        logger.info("Starting login")
        email_form = self.browser.find_element(
            *LoginPageLocators.REGISTER_EMAIL
        )
        email_form.send_keys(email)

        password_form = self.browser.find_element(
            *LoginPageLocators.REGISTER_PASSWORD
        )
        password_form.send_keys(password)

        login_button = self.browser.find_element(
            *LoginPageLocators.LOGIN_BUTTON
        )
        login_button.click()
