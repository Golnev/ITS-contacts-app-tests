"""
This module provides methods for interacting with the "Contact Details" page.
"""

import logging as logger
import time
from typing import Literal

from src.locators import ContactDetailsPageLocators
from src.pages.base_page import BasePage


class ContactDetailsPage(BasePage):
    """
    Class with methods for verifying and interacting
    with the 'Contact Details' page.
    """

    def should_be_contact_details_page(self):
        """
        Verify that the current page is the 'Contact Details' page.
        """

        self.should_be_contact_details_page_url()
        self.should_be_contact_details_form()

    def should_be_contact_details_page_url(self):
        """
        Verify that the current page URL
        matches the expected 'Contact Details' page URL.
        """

        logger.info("Check contacts details page url.")

        assert (
            self.browser.current_url
            == ContactDetailsPageLocators.CONTACT_DETAILS_PAGE_URL
        ), "URL address is not correct."

    def should_be_contact_details_form(self):
        """
        Verify the presence of the contact details form on the page.
        """

        logger.info("Check contact details form is present.")

        assert self.is_element_present(
            *ContactDetailsPageLocators.CONTACT_DETAILS_FORM
        ), "Contact details form is not present."

    def logout(self):
        """
        Log out the current user from the 'Contact Details' page.
        """

        logger.info("Logout.")

        logout_button = self.browser.find_element(
            *ContactDetailsPageLocators.LOGOUT_BUTTON
        )
        logout_button.click()

    def return_to_contact_list(self):
        """
        Return to the contact list from the 'Contact Details' page.
        """

        logger.info("Return to contact list.")

        return_button = self.browser.find_element(
            *ContactDetailsPageLocators.RETURN_BUTTON
        )
        return_button.click()

    def delete_contact(self):
        """
        Delete the current contact from the 'Contact Details' page.
        """

        logger.info("Deleting contact.")

        delete_button = self.browser.find_element(
            *ContactDetailsPageLocators.DELETE_BUTTON
        )
        delete_button.click()

        alert = self.browser.switch_to.alert
        alert.accept()

    def go_to_edit_contact_page(self):
        """
        Navigate to the 'Edit Contact' page
        from the 'Contact Details' page.
        """

        logger.info("Go to edit contact page.")

        edit_contact_button = self.browser.find_element(
            *ContactDetailsPageLocators.EDIT_CONTACT_BUTTON
        )
        edit_contact_button.click()

    def get_info(
        self,
        what: Literal[
            "first_name",
            "last_name",
            "date_of_birth",
            "email",
            "phone",
            "street_address_1",
            "street_address_2",
            "city",
            "state",
            "postal_code",
            "country",
        ],
    ):
        """
        Retrieve information from a specified field
        on the 'Contact Details' page.
        """

        logger.info("Get info from field.")

        locators_dict = {
            "first_name": ContactDetailsPageLocators.FIRST_NAME,
            "last_name": ContactDetailsPageLocators.LAST_NAME,
            "date_of_birth": ContactDetailsPageLocators.DATE_OF_BIRTH,
            "email": ContactDetailsPageLocators.EMAIL,
            "phone": ContactDetailsPageLocators.PHONE,
            "street_address_1": ContactDetailsPageLocators.STREET_ADDRESS_1,
            "street_address_2": ContactDetailsPageLocators.STREET_ADDRESS_2,
            "city": ContactDetailsPageLocators.CITY,
            "state": ContactDetailsPageLocators.STATE,
            "postal_code": ContactDetailsPageLocators.POSTAL_CODE,
            "country": ContactDetailsPageLocators.COUNTRY,
        }

        time.sleep(3)
        field_text = self.get_visible_element_text(*locators_dict[what])

        return field_text
