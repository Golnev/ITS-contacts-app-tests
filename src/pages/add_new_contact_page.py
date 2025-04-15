"""
This module provides methods for interacting with the "Add New Contact" page.
"""

import logging as logger

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
            self.browser.current_url == AddNewContactPageLocators.ADD_NEW_CONTACT_PAGE_URL
        ), "URL address is not correct."

    def should_be_add_new_contact_form(self):
        """
        Method for verifying that the 'Add New Contact form' is correct.
        """

        logger.info("Check add new contact form is present.")

        assert self.is_element_present(
            *AddNewContactPageLocators.ADD_NEW_CONTACT_FORM
        ), "Add new contact form is not present."

    def cancel_from_add_new_contact_page(self):
        """
        Method to cancel form add new page by clicking the cancel button.
        """

        logger.info("Cancel from add new contact page")

        self.click_button(locator=AddNewContactPageLocators.CANCEL_BUTTON)

    def add_new_contact(
        self,
        contact_info: dict,
    ):
        """
        Method to add new contact.
        """

        logger.info(
            "Add new contact, with first name: %s, last name: %s",
            contact_info["firstName"],
            contact_info["lastName"],
        )

        self.send_text(
            locator=AddNewContactPageLocators.FIRST_NAME,
            text=contact_info["firstName"],
        )

        self.send_text(
            locator=AddNewContactPageLocators.LAST_NAME,
            text=contact_info["lastName"],
        )

        self.send_text(
            locator=AddNewContactPageLocators.DATE_OF_BIRTH,
            text=contact_info["birthdate"],
        )

        self.send_text(
            locator=AddNewContactPageLocators.EMAIL,
            text=contact_info["email"],
        )

        self.send_text(
            locator=AddNewContactPageLocators.PHONE,
            text=str(contact_info["phone"]),
        )

        self.send_text(
            locator=AddNewContactPageLocators.STREET_ADDRESS_1,
            text=contact_info["street1"],
        )

        self.send_text(
            locator=AddNewContactPageLocators.CITY,
            text=contact_info["city"],
        )

        self.send_text(
            locator=AddNewContactPageLocators.STATE,
            text=contact_info["stateProvince"],
        )

        self.send_text(
            locator=AddNewContactPageLocators.POSTAL_CODE,
            text=str(contact_info["postalCode"]),
        )

        self.send_text(
            locator=AddNewContactPageLocators.COUNTRY,
            text=contact_info["country"],
        )

        self.click_button(locator=AddNewContactPageLocators.SUBMIT_BUTTON)
