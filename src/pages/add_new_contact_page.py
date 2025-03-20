"""
This module provides methods for interacting with the "Add New Contact" page.
"""

import logging as logger
import time

from src.locators import AddNewContactPageLocators
from src.pages.base_page import BasePage


class AddNewContactPage(BasePage):
    """
    Class with methods for verifying the 'Add New Contact' page.
    """

    def should_be_add_new_contact_page(self):
        """
        Method for verifying that the 'Add New Contact' page is correct.
        """

        self.should_be_contact_list_url()
        self.should_be_add_new_contact_form()

    def should_be_contact_list_url(self):
        """
        Method for verifying that the 'contact list' page url is correct.
        """

        logger.info("Check contact list url.")

        assert (
            self.browser.current_url
            == AddNewContactPageLocators.ADD_NEW_CONTACT_PAGE_URL
        ), "URL address is not correct."

    def should_be_add_new_contact_form(self):
        """
        Method for verifying that the 'Add New Contact form' is correct.
        """

        logger.info("Check add new contact form is present.")

        assert self.is_element_present(
            *AddNewContactPageLocators.ADD_NEW_CONTACT_FORM
        ), "Add new contact form is not present."

    def logout(self):
        """
        Method to log out the current user by clicking the logout button.
        """

        logger.info("Logout.")

        logout_button = self.browser.find_element(
            *AddNewContactPageLocators.LOGOUT_BUTTON
        )
        logout_button.click()

    def cancel_from_add_new_contact_page(self):
        """
        Method to cancel form add new page by clicking the cancel button.
        """

        logger.info("Cancel from add new contact page")

        cancel_button = self.wait_for_element_ready(
            AddNewContactPageLocators.CANCEL_BUTTON
        )

        cancel_button.click()

    def add_new_contact(
        self,
        first_name,
        last_name,
        date_of_birth,
        email,
        phone,
        street_address_1,
        city,
        state,
        postal_code,
        country,
    ):
        """
        Method to add new contact.
        """

        logger.info(
            "Add new contact, with first name: %s, last name: %s",
            first_name,
            last_name,
        )

        time.sleep(5)

        first_name_form = self.wait_for_element_ready(
            AddNewContactPageLocators.FIRST_NAME
        )

        first_name_form.send_keys(first_name)

        last_name_form = self.wait_for_element_ready(
            AddNewContactPageLocators.LAST_NAME
        )
        last_name_form.send_keys(last_name)

        date_of_birth_form = self.wait_for_element_ready(
            AddNewContactPageLocators.DATE_OF_BIRTH
        )
        date_of_birth_form.send_keys(date_of_birth)

        email_form = self.wait_for_element_ready(
            AddNewContactPageLocators.EMAIL
        )
        email_form.send_keys(email)

        phone_form = self.wait_for_element_ready(
            AddNewContactPageLocators.PHONE
        )
        phone_form.send_keys(str(phone))

        street_address_1_form = self.wait_for_element_ready(
            AddNewContactPageLocators.STREET_ADDRESS_1
        )
        street_address_1_form.send_keys(street_address_1)

        city_form = self.wait_for_element_ready(AddNewContactPageLocators.CITY)
        city_form.send_keys(city)

        state_form = self.wait_for_element_ready(
            AddNewContactPageLocators.STATE
        )
        state_form.send_keys(state)

        postal_code_form = self.wait_for_element_ready(
            AddNewContactPageLocators.POSTAL_CODE
        )
        postal_code_form.send_keys(str(postal_code))

        country_form = self.wait_for_element_ready(
            AddNewContactPageLocators.COUNTRY
        )
        country_form.send_keys(country)

        submit_button = self.wait_for_element_ready(
            AddNewContactPageLocators.SUBMIT_BUTTON
        )
        submit_button.click()

        time.sleep(5)
