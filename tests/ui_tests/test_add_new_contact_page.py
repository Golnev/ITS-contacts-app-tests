"""
This module contains UI tests
for the "Add New Contact" page using Selenium WebDriver.
"""

import logging as logger

import pytest
from selenium import webdriver

from src.helpers.contacts_helper import ContactsHelper
from src.pages.add_new_contact_page import AddNewContactPage
from src.pages.contact_list_page import ContactListPage
from src.requests_utilities import RequestUtilities


base_url = RequestUtilities.get_base_url()


@pytest.mark.ui
@pytest.mark.add_new_contact_page
@pytest.mark.usefixtures("del_all_contacts", "setup_user")
class TestAddNewContactPage:
    """
    Test suite for the "Add New Contact" page.
    """

    logger.info("Starting tests for add new contact page.")

    def test_user_should_be_in_add_new_contact_page(self, browser: webdriver.Firefox | webdriver.Chrome):
        """
        Verify navigation to the "Add New Contact" page.
        """

        logger.info("Starting Test: user should be in add new contact page")

        link = base_url + "addContact"
        page = AddNewContactPage(browser=browser, url=link)
        page.open()
        page.should_be_add_new_contact_page()

    def test_logout_from_add_new_contact_page(self, browser: webdriver.Firefox | webdriver.Chrome):
        """
        Test logout functionality from the "Add New Contact" page.
        """

        logger.info("Starting Test: logout from add new contact page")

        link = base_url + "addContact"
        page = AddNewContactPage(browser=browser, url=link)
        page.open()

        page.logout()

        assert page.browser.current_url == base_url, f"Wrong URL after logout. URL: {page.browser.current_url}"

    def test_cancel_from_add_new_contact_page(self, browser: webdriver.Firefox | webdriver.Chrome):
        """
        Verify the cancel operation on the "Add New Contact" page.
        """

        logger.info("Starting Test: cancel from add new contact page")

        link = base_url + "addContact"
        page = AddNewContactPage(browser=browser, url=link)
        page.open()

        page.is_url_change(base_url + "addContact")

        page.cancel_from_add_new_contact_page()

        page.is_url_change(base_url + "contactList")

        contact_list_page = ContactListPage(browser=browser, url=browser.current_url)
        contact_list_page.should_be_contact_list_page()

    def test_add_new_contact(
        self,
        browser: webdriver.Firefox | webdriver.Chrome,
    ):
        """
        Verify that a new contact can be added successfully.
        """

        contact_info = ContactsHelper.fake_contact()

        logger.info("Starting Test: add new contact")

        link = base_url + "addContact"
        page = AddNewContactPage(browser=browser, url=link)
        page.open()

        page.add_new_contact(contact_info)

        page.is_url_change(base_url + "contactList")

        assert (
            page.browser.current_url == base_url + "contactList"
        ), f"Wrong URL after add new contact. URL: {page.browser.current_url}"

        contact_list_page = ContactListPage(browser=browser, url=browser.current_url)
        contact_list_page.find_contact_by_full_name(
            first_name=contact_info["firstName"],
            last_name=contact_info["lastName"],
        )
