"""
This module sets up configurations, fixtures, and helpers
for running Selenium-based and API-based tests.
"""

# pylint: disable=import-outside-toplevel
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

import logging as logger
import os

import pytest
from dotenv import load_dotenv
from faker import Faker
from selenium import webdriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.helpers.contacts_helper import ContactsHelper
from src.pages.add_new_contact_page import AddNewContactPage
from src.pages.contact_details_page import ContactDetailsPage
from src.pages.contact_list_page import ContactListPage
from src.pages.login_page import LoginPage
from src.requests_utilities import RequestUtilities

load_dotenv()

firefox_path = os.getenv("FIREFOX_PATH")
geckodriver_path = os.getenv("GECKODRIVER_PATH")

google_chrome_path = os.getenv("GOOGLE_CHROME_PATH")
chromedriver_path = os.getenv("CHROMEDRIVER_PATH")

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


@pytest.fixture(scope="module")
def auth_headers():
    """Provides authorization headers for API requests."""

    my_email = os.getenv("MY_EMAIL")
    my_pass = os.getenv("MY_PASSWORD")

    request_utility = RequestUtilities()

    logger.info("Login with My Email.")
    response_json = request_utility.post(
        endpoint="users/login",
        payload={"email": my_email, "password": my_pass},
    )

    assert (
        response_json is not None
    ), "Response is None, but expected JSON response."
    token = response_json["token"]

    yield {"Authorization": f"Bearer {token}"}

    logger.info("Logout.")
    request_utility.post(
        endpoint="users/logout", headers={"Authorization": f"Bearer {token}"}
    )


@pytest.fixture()
def manage_contacts(auth_headers, pytestconfig):
    """Manages contact creation and cleanup for API tests."""

    contacts_helper = ContactsHelper()
    created_contacts = []

    def create_contact():
        contact_rs_api, contact_info = contacts_helper.create_contact(
            auth_headers=auth_headers
        )
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
                contact = contacts_helper.get_contacts(
                    auth_headers=auth_headers, contact_id=contact_id
                )
                if contact:
                    contacts_helper.delete_contact(
                        auth_headers=auth_headers, contact_id=contact_id
                    )
                    logger.info("Deleted contact: %s", contact_id)
            except AssertionError as e:
                logger.info(
                    "Contact %s already deleted or not found: %s",
                    contact_id,
                    e,
                )
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error(
                    "Error while trying to delete contact %s: %s",
                    contact_id,
                    e,
                )


@pytest.fixture
def browser(pytestconfig):
    """Initializes a Selenium WebDriver instance for the specified browser."""

    browser_name = pytestconfig.getoption("--browser_name")
    browser_driver = None

    if browser_name == "firefox":
        logger.info("Prepare browser firefox.")

        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver.firefox.service import Service

        options = Options()
        if firefox_path and geckodriver_path:
            options.binary_location = firefox_path

            service = Service(executable_path=geckodriver_path)
            browser_driver = webdriver.Firefox(
                service=service, options=options
            )
    elif browser_name == "chrome":
        logger.info("Prepare browser chrome.")

        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service

        options = Options()
        if google_chrome_path and chromedriver_path:
            options.binary_location = google_chrome_path

            service = Service(executable_path=chromedriver_path)
            browser_driver = webdriver.Chrome(service=service, options=options)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")

    yield browser_driver

    logger.info("Browser quit.")
    if browser_driver:
        browser_driver.quit()


@pytest.fixture()
def del_all_contacts(
    request, pytestconfig, browser: webdriver.Firefox | webdriver.Chrome
):
    """Deletes all test contacts from the contact list page (Selenium-based cleanup)."""

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
    """Logs in a user using the login page."""

    logger.info("Setup user with default parameters.")
    link = base_url + "login"
    page = LoginPage(browser=browser, url=link)
    page.open()

    email = os.getenv("MY_EMAIL")
    password = os.getenv("MY_PASSWORD")

    if email and password:
        page.login(email=email, password=password)


@pytest.fixture(scope="function")
def create_contact_info(
    browser: webdriver.Firefox | webdriver.Chrome, setup_user
):
    """Creates contact information using the Faker library."""

    logger.info("Create contact.")
    link = base_url + "addContact"
    page = AddNewContactPage(browser=browser, url=link)
    page.open()

    fake = Faker()
    fake_contact_first_name = fake.first_name()
    fake_contact_last_name = fake.last_name()
    fake_contact_date_of_birth = (
        fake.date_of_birth(minimum_age=6, maximum_age=110)
    ).strftime("%Y-%m-%d")
    fake_contact_email = fake.email()
    fake_contact_phone = fake.basic_phone_number()
    fake_contact_street_address_1 = fake.street_name()
    fake_contact_city = fake.city()
    fake_contact_state = fake.state()
    fake_contact_postal_code = fake.postalcode()
    fake_contact_country = fake.country()[:40]

    return (
        fake_contact_first_name,
        fake_contact_last_name,
        fake_contact_date_of_birth,
        fake_contact_email,
        fake_contact_phone,
        fake_contact_street_address_1,
        fake_contact_city,
        fake_contact_state,
        fake_contact_postal_code,
        fake_contact_country,
    )


@pytest.fixture(scope="function")
def created_contact(
    browser: webdriver.Firefox | webdriver.Chrome,
    setup_user,
    create_contact_info,
    pytestconfig,
):
    """Creates a new contact using Selenium."""

    logger.info(
        "Creating contact with Contact first name: %s, last name: %s",
        create_contact_info[0],
        create_contact_info[1],
    )

    add_new_contact_link = base_url + "addContact"
    page = AddNewContactPage(browser=browser, url=add_new_contact_link)
    page.open()

    page.add_new_contact(*create_contact_info)

    WebDriverWait(browser, 10).until(EC.url_to_be(base_url + "contactList"))

    contact_list_page = ContactListPage(
        browser=browser, url=browser.current_url
    )

    contact_list_page.go_to_contact_details_by_full_name(
        first_name=create_contact_info[0], last_name=create_contact_info[1]
    )

    contact_details_page = ContactDetailsPage(
        browser=browser, url=browser.current_url
    )

    return contact_details_page, create_contact_info
