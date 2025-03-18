"""
This module provides methods for interacting with the "Contact List" page.
"""

import logging as logger

from selenium.webdriver.common.by import By

from src.locators import ContactListPageLocators
from src.pages.base_page import BasePage


class ContactListPage(BasePage):
    """
    Class with methods for verifying
    and interacting with the 'Contact List' page.
    """

    def should_be_contact_list_page(self):
        """
        Verify that the current page is the 'Contact List' page.
        """

        self.should_be_contact_list_url()
        self.should_be_add_new_contact_button()
        self.should_be_contact_list_table()

    def should_be_contact_list_url(self):
        """
        Verify that the URL of the current page
        matches the expected 'Contact List' page URL.
        """

        logger.info("Check contact list url.")

        assert (
            self.browser.current_url
            == ContactListPageLocators.CONTACT_LIST_PAGE_URL
        ), "URL address is not correct."

    def should_be_add_new_contact_button(self):
        """
        Verify the presence of the 'Add New Contact' button on the page.
        """

        logger.info("Check add new contact button is present.")

        assert self.is_element_present(
            *ContactListPageLocators.ADD_NEW_CONTACT_BUTTON
        ), "Add new contact button is not present."

    def should_be_contact_list_table(self):
        """
        Verify the presence of the contact list table on the page.
        """

        logger.info("Check contact list table is present.")

        assert self.is_element_present(
            *ContactListPageLocators.CONTACT_LIST_TABLE
        ), "Contact list table is not present."

    def logout(self):
        """
        Log out the current user from the 'Contact List' page.
        """

        logger.info("Logout.")

        logout_button = self.browser.find_element(
            *ContactListPageLocators.LOGOUT_BUTTON
        )
        logout_button.click()

    def go_to_add_new_contact(self):
        """
        Navigate to the 'Add New Contact' page.
        """

        logger.info("Go to add new contact page.")

        add_new_contact_button = self.browser.find_element(
            *ContactListPageLocators.ADD_NEW_CONTACT_BUTTON
        )
        add_new_contact_button.click()

    def find_contact_by_full_name(self, first_name: str, last_name: str):
        """
        Search for a contact by their full name
        in the contact list table.
        """

        logger.info("Find contact by full name.")

        full_name = " ".join([first_name, last_name])
        rows = self.browser.find_elements(
            *ContactListPageLocators.FULL_NAME_CONTACTS
        )

        list_of_all_full_names = [row.text for row in rows]

        assert (
            full_name in list_of_all_full_names
        ), f"{first_name} {last_name} not in the contact list."

    def contact_is_not_present_in_contact_list(
        self, first_name: str, last_name: str
    ):
        """
        Verify that a contact with the specified full name
        is not present in the contact list table.
        """

        full_name = " ".join([first_name, last_name])

        rows = self.browser.find_elements(
            *ContactListPageLocators.FULL_NAME_CONTACTS
        )

        list_of_all_full_names = [row.text for row in rows]

        assert (
            full_name not in list_of_all_full_names
        ), f"{first_name} {last_name} in the contact list."

    def go_to_contact_details_by_full_name(
        self, first_name: str, last_name: str
    ):
        """
        Navigate to the 'Contact Details' page for a specified contact.
        """

        logger.info("Go to contact details by full name.")

        full_name = " ".join([first_name, last_name])
        contact = self.browser.find_element(
            By.XPATH, f"//table//td[contains(text(), '{full_name}')]"
        )
        contact.click()

    def get_first_contact(self):
        """
        Retrieve the first contact from the contact list table.
        """

        logger.info("Get first contact from list.")

        if self.is_element_present(*ContactListPageLocators.FIRST_CONTACT):
            first_contact = self.browser.find_element(
                *ContactListPageLocators.FIRST_CONTACT
            )
            return first_contact

        logger.info("No contacts.")
        return None
