"""
This module contains UI tests
for the "Contact Details" page using Selenium WebDriver.
"""

import logging as logger

import pytest
from selenium import webdriver

from src.pages.contact_details_page import ContactDetailsPage
from src.pages.contact_list_page import ContactListPage
from src.pages.edit_contact_page import EditContactPage
from src.requests_utilities import RequestUtilities


base_url = RequestUtilities.get_base_url()


@pytest.mark.ui
@pytest.mark.contact_details_page
@pytest.mark.usefixtures("del_all_contacts")
class TestContactDetailsPage:
    """
    Test suite for the "Contact Details" page.
    """

    logger.info("Starting tests for contact details page.")

    def test_user_should_be_in_contact_details_page(
        self,
        created_contact: tuple[ContactDetailsPage, dict],
    ):
        """
        Verifies that the user is on the "Contact Details" page.
        """

        logger.info("Starting Test: user should be in contact details page.")

        page, _ = created_contact

        page.should_be_contact_details_page()

    @pytest.mark.usefixtures("browser")
    def test_logout_from_contact_details_page(
        self,
        created_contact: tuple[ContactDetailsPage, dict],
    ):
        """
        Verifies that the user can log out
        from the "Contact Details" page.
        """

        logger.info("Starting Test: logout from contact details page.")

        page, _ = created_contact

        page.logout()

        assert page.browser.current_url == base_url, f"Wrong URL after logout. URL: {page.browser.current_url}"

    def test_return_to_contact_list(
        self,
        browser: webdriver.Firefox | webdriver.Chrome,
        created_contact: tuple[ContactDetailsPage, dict],
    ):
        """
        Verifies that the user can return to the contact list
        from the "Contact Details" page.
        """

        logger.info("Starting Test: return to contact list.")

        page, _ = created_contact

        page.return_to_contact_list()

        contact_list_page = ContactListPage(browser=browser, url=browser.current_url)
        contact_list_page.should_be_contact_list_page()

    def test_delete_contact(
        self,
        browser: webdriver.Firefox | webdriver.Chrome,
        created_contact: tuple[ContactDetailsPage, dict],
    ):
        """
        Verifies that a contact can be deleted from
        the "Contact Details" page.
        """

        logger.info("Starting Test: delete contact.")

        page, contact_info = created_contact

        page.delete_contact()

        page.is_url_change(base_url + "contactList")

        contact_list_page = ContactListPage(browser=browser, url=browser.current_url)
        contact_list_page.should_be_contact_list_page()
        contact_list_page.contact_is_not_present_in_contact_list(
            first_name=contact_info["firstName"],
            last_name=contact_info["lastName"],
        )

    def test_user_can_go_to_edit_contact(
        self,
        browser: webdriver.Firefox | webdriver.Chrome,
        created_contact: tuple[ContactDetailsPage, dict],
    ):
        """
        Verifies that the user can navigate to the "Edit Contact" page
        from the "Contact Details" page.
        """

        logger.info("Starting Test: user can go to edit contact.")

        page, _ = created_contact

        page.go_to_edit_contact_page()

        page.is_url_change(base_url + "editContact")

        edit_contact_page = EditContactPage(browser=browser, url=browser.current_url)
        edit_contact_page.should_be_edit_contact_page()
