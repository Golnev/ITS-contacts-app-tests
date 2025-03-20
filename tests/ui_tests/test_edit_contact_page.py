"""
This module contains UI tests
for the "Edit Contact" page using Selenium WebDriver.
"""

import logging as logger

import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.pages.contact_details_page import ContactDetailsPage
from src.pages.edit_contact_page import EditContactPage
from src.requests_utilities import RequestUtilities

pytestmark = pytest.mark.ui

base_url = RequestUtilities.get_base_url()


@pytest.mark.edit_contact_page
@pytest.mark.usefixtures("del_all_contacts")
class TestEditContactPage:
    """
    Test suite for the "Edit Contact" page.
    """

    logger.info("Starting tests for edit contact page.")

    def test_user_should_be_in_edit_contact_page(
        self,
        browser: webdriver.Firefox | webdriver.Chrome,
        setup_user,
        created_contact: tuple[ContactDetailsPage, tuple],
    ):
        """
        Verifies that the user is on the "Edit Contact" page.
        """

        logger.info("Starting Test: user should be in edit contact page")

        contact_page, _ = created_contact
        contact_page.go_to_edit_contact_page()

        page = EditContactPage(browser=browser, url=browser.current_url)

        page.should_be_edit_contact_page()

    def test_logout_from_edit_contact_page(
        self,
        browser: webdriver.Firefox | webdriver.Chrome,
        setup_user,
        created_contact: tuple[ContactDetailsPage, tuple],
    ):
        """
        Verifies that the user can log out from the "Edit Contact" page.
        """

        logger.info("Starting Test: logout from edit contact page")

        contact_page, _ = created_contact
        contact_page.go_to_edit_contact_page()

        page = EditContactPage(browser=browser, url=browser.current_url)

        page.logout()

        WebDriverWait(browser, 10).until(EC.url_to_be(base_url))

        assert (
            page.browser.current_url == base_url
        ), f"Wrong URL after logout. URL: {page.browser.current_url}"

    def test_return_to_contact_details(
        self,
        browser: webdriver.Firefox | webdriver.Chrome,
        setup_user,
        created_contact: tuple[ContactDetailsPage, tuple],
    ):
        """
        Verifies that the user can return to the "Contact Details" page
        from the "Edit Contact" page.
        """

        logger.info(
            "Starting Test: return to contact details from edit contact page."
        )

        contact_page, _ = created_contact
        contact_page.go_to_edit_contact_page()

        page = EditContactPage(browser=browser, url=browser.current_url)

        page.return_to_contact_details()

        contact_details_page = ContactDetailsPage(
            browser=browser, url=browser.current_url
        )
        contact_details_page.should_be_contact_details_page()

    def test_edit_contact_phone(
        self,
        browser: webdriver.Firefox | webdriver.Chrome,
        setup_user,
        created_contact: tuple[ContactDetailsPage, tuple],
    ):
        """
        Verifies that the user can edit a contact's phone number.
        """

        logger.info("Starting test: edit contact.")

        contact_page, _ = created_contact
        contact_page.go_to_edit_contact_page()

        page = EditContactPage(browser=browser, url=browser.current_url)

        fake = Faker()
        fake_new_phone = fake.basic_phone_number()

        page.edit_contact(what="phone", data=fake_new_phone)

        contact_details_page = ContactDetailsPage(
            browser=browser, url=browser.current_url
        )

        new_phone = contact_details_page.get_info(what="phone")

        assert fake_new_phone == new_phone, (
            f"Incorrect phone number of a contact\n"
            f"Expected: {fake_new_phone}, received: {new_phone}"
        )
