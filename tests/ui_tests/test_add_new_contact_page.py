"""
This module contains UI tests for the "Add New Contact" page using Selenium WebDriver.
"""

# pylint: disable=unused-argument

import logging as logger

import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.pages.add_new_contact_page import AddNewContactPage
from src.pages.contact_list_page import ContactListPage
from src.requests_utilities import RequestUtilities

pytestmark = pytest.mark.ui

base_url = RequestUtilities.get_base_url()


@pytest.mark.add_new_contact_page
@pytest.mark.usefixtures("del_all_contacts")
class TestAddNewContactPage:
    """Test suite for the "Add New Contact" page."""

    logger.info("Starting tests for add new contact page.")

    def test_user_should_be_in_add_new_contact_page(
        self, browser: webdriver.Firefox | webdriver.Chrome, setup_user
    ):
        """Verify navigation to the "Add New Contact" page."""

        logger.info("Starting Test: user should be in add new contact page")

        link = base_url + "addContact"
        page = AddNewContactPage(browser=browser, url=link)
        page.open()
        page.should_be_add_new_contact_page()

    def test_logout_from_add_new_contact_page(
        self, browser: webdriver.Firefox | webdriver.Chrome, setup_user
    ):
        """Test logout functionality from the "Add New Contact" page."""

        logger.info("Starting Test: logout from add new contact page")

        link = base_url + "addContact"
        page = AddNewContactPage(browser=browser, url=link)
        page.open()

        page.logout()

        WebDriverWait(browser, 10).until(EC.url_to_be(base_url))

        assert (
            page.browser.current_url == base_url
        ), f"Wrong URL after logout. URL: {page.browser.current_url}"

    def test_cancel_from_add_new_contact_page(
        self, browser: webdriver.Firefox | webdriver.Chrome, setup_user
    ):
        """Verify the cancel operation on the "Add New Contact" page."""

        logger.info("Starting Test: cancel from add new contact page")

        link = base_url + "addContact"
        page = AddNewContactPage(browser=browser, url=link)
        page.open()

        page.cancel_from_add_new_contact_page()

        WebDriverWait(browser, 5).until(EC.url_changes(link))

        contact_list_page = ContactListPage(
            browser=browser, url=browser.current_url
        )
        contact_list_page.should_be_contact_list_page()

    def test_add_new_contact(
        self,
        browser: webdriver.Firefox | webdriver.Chrome,
        setup_user,
        create_contact_info,
    ):
        """Verify that a new contact can be added successfully."""

        logger.info("Starting Test: add new contact")

        link = base_url + "addContact"
        page = AddNewContactPage(browser=browser, url=link)
        page.open()

        page.add_new_contact(*create_contact_info)

        WebDriverWait(browser, 10).until(
            EC.url_to_be(base_url + "contactList")
        )

        assert (
            page.browser.current_url == base_url + "contactList"
        ), f"Wrong URL after add new contact. URL: {page.browser.current_url}"

        contact_list_page = ContactListPage(
            browser=browser, url=browser.current_url
        )
        contact_list_page.find_contact_by_full_name(
            first_name=create_contact_info[0], last_name=create_contact_info[1]
        )
