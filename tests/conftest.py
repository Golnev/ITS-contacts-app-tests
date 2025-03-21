"""
This module sets up configurations, fixtures, and helpers
for running Selenium-based and API-based tests.
"""

import logging as logger
import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from src.helpers.contacts_helper import ContactsHelper
from src.pages.add_new_contact_page import AddNewContactPage
from src.pages.contact_details_page import ContactDetailsPage
from src.pages.contact_list_page import ContactListPage
from src.pages.login_page import LoginPage
from src.requests_utilities import RequestUtilities

load_dotenv()

base_url = RequestUtilities.get_base_url()


def pytest_addoption(parser):
    """
    Add custom command-line options for Pytest.

    Options:
    - `--rm`: Enables automatic deletion of created contacts after tests.
    - `--browser_name`: Specifies the browser to use (chrome or firefox).
    """

    parser.addoption(
        "--rm",
        action="store_true",
        default=False,
        help="Delete a created contact after a test",
    )
    parser.addoption(
        "--browser_name",
        action="store",
        default="firefox",
        help="Choose browser: chrome or firefox",
    )


@pytest.fixture()
def manage_contacts(pytestconfig):
    """
    Manages contact creation and cleanup for API tests.
    """

    contacts_helper = ContactsHelper()
    created_contacts = []

    def create_contact():
        contact_rs_api, contact_info = contacts_helper.create_contact()
        assert (
            contact_rs_api is not None
        ), "Response is None, but expected JSON response."
        create_contact_id = contact_rs_api["_id"]
        created_contacts.append(create_contact_id)
        return contact_rs_api, contact_info

    yield create_contact

    if pytestconfig.getoption("--rm"):
        for contact_id in created_contacts:
            try:
                contact = contacts_helper.get_contacts(contact_id=contact_id)
                if contact:
                    contacts_helper.delete_contact(contact_id=contact_id)
                    logger.info("Deleted contact: %s", contact_id)
            except AssertionError as e:
                logger.info(
                    "Contact %s already deleted or not found: %s",
                    contact_id,
                    e,
                )


@pytest.fixture
def browser(pytestconfig):
    """
    Initializes a Selenium WebDriver instance for the specified browser.
    """

    browser_name = pytestconfig.getoption("--browser_name")

    if browser_name == "firefox":
        logger.info("Prepare browser firefox.")

        options = Options()
        firefox_path = os.getenv("FIREFOX_PATH")

        if firefox_path:
            options.binary_location = firefox_path

            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options,
            )
        else:
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install())
            )

    elif browser_name == "chrome":
        logger.info("Prepare browser chrome.")

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install())
        )

    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")

    yield driver

    logger.info("Browser quit.")
    if driver:
        driver.quit()


@pytest.fixture()
def del_all_contacts(
    pytestconfig, browser: webdriver.Firefox | webdriver.Chrome
):
    """
    Deletes all test contacts from the contact list page
    (Selenium-based cleanup).
    """

    yield
    if pytestconfig.getoption("--rm"):
        logger.info("Delete all contacts.")
        link = base_url + "contactList"
        contact_list_page = ContactListPage(browser=browser, url=link)
        contact_list_page.open()

        while True:
            first_contact = contact_list_page.get_first_contact()

            if first_contact:
                WebDriverWait(browser, 5).until(
                    EC.element_to_be_clickable(first_contact)
                )
                first_contact.click()
                contact_details_page = ContactDetailsPage(
                    browser=browser, url=browser.current_url
                )
                contact_details_page.delete_contact()
                WebDriverWait(browser, 5).until(EC.staleness_of(first_contact))
                contact_list_page.open()
            else:
                break


@pytest.fixture(scope="function")
def setup_user(browser: webdriver.Firefox | webdriver.Chrome):
    """
    Logs in a user using the login page.
    """

    logger.info("Setup user with default parameters.")
    link = base_url + "login"
    page = LoginPage(browser=browser, url=link)
    page.open()

    email = os.getenv("MY_EMAIL")
    password = os.getenv("MY_PASSWORD")

    if email and password:
        page.login(email=email, password=password)

    WebDriverWait(browser, 10).until(EC.url_to_be(base_url + "contactList"))


@pytest.fixture(scope="function")
def created_contact(
    browser: webdriver.Firefox | webdriver.Chrome,
    setup_user,
):
    """
    Creates a new contact using Selenium.
    """

    contact_info = ContactsHelper.fake_contact()

    logger.info(
        "Creating contact with Contact first name: %s, last name: %s",
        contact_info["firstName"],
        contact_info["lastName"],
    )

    add_new_contact_link = base_url + "addContact"
    page = AddNewContactPage(browser=browser, url=add_new_contact_link)
    page.open()

    WebDriverWait(browser, 10).until(EC.url_to_be(base_url + "addContact"))

    page.add_new_contact(contact_info=contact_info)

    WebDriverWait(browser, 10).until(EC.url_to_be(base_url + "contactList"))

    contact_list_page = ContactListPage(
        browser=browser, url=browser.current_url
    )

    contact_list_page.go_to_contact_details_by_full_name(
        first_name=contact_info["firstName"],
        last_name=contact_info["lastName"],
    )

    contact_details_page = ContactDetailsPage(
        browser=browser, url=browser.current_url
    )

    return contact_details_page, contact_info
