"""
This module provides methods for interacting with the "Register" page.
"""

import logging as logger

from src.locators import RegisterPageLocators
from src.pages.base_page import BasePage


class RegisterPage(BasePage):
    """
    Class for interacting with the 'Register' page.
    """

    def should_be_register_page(self):
        """
        Verify that the current page is the 'Register' page.
        """

        self.should_be_register_url()
        self.should_be_register_form()

    def should_be_register_url(self):
        """
        Verify that the URL of the current page
        matches the expected 'Register' page URL.
        """

        logger.info("Check register url.")
        assert (
            self.browser.current_url == RegisterPageLocators.REGISTER_PAGE_URL
        ), "URL address is not correct."

    def should_be_register_form(self):
        """
        Verify the presence of the registration form on the page.
        """

        logger.info("Check register form is present.")
        assert self.is_element_present(
            *RegisterPageLocators.REGISTER_FORM
        ), "Register form is not presented."

    def register_new_user(
        self, first_name: str, last_name: str, email: str, password: str
    ):
        """
        Register a new user with the provided credentials.
        """

        logger.info("Starting register new user.")

        first_name_form = self.browser.find_element(
            *RegisterPageLocators.REGISTER_FIRST_NAME
        )
        first_name_form.send_keys(first_name)

        last_name_form = self.browser.find_element(
            *RegisterPageLocators.REGISTER_LAST_NAME
        )
        last_name_form.send_keys(last_name)

        email_form = self.browser.find_element(
            *RegisterPageLocators.REGISTER_EMAIL
        )
        email_form.send_keys(email)

        password_form = self.browser.find_element(
            *RegisterPageLocators.REGISTER_PASSWORD
        )
        password_form.send_keys(password)

        register_button = self.browser.find_element(
            *RegisterPageLocators.REGISTER_BUTTON
        )
        register_button.click()

    def should_be_validation_error(self):
        """
        Verify that a validation error notification
        is displayed on the 'Register' page.
        """

        logger.info("Check validation error notification.")
        assert self.get_visible_element_text(
            *RegisterPageLocators.ERROR_NOTIFICATION
        ).startswith(
            "User validation failed"
        ), "Error notification is not presented."

    def cancel_from_register_page(self):
        """
        Cancel the registration process
        and navigate away from the 'Register' page.
        """

        logger.info("Cancel from register page")

        cancel_button = self.browser.find_element(
            *RegisterPageLocators.CANCEL_BUTTON
        )
        cancel_button.click()
