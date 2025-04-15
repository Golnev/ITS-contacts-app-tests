"""
This module provides methods for interacting with the "Base" page.
"""

import logging as logger
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.locators import BasePageLocators
from src.requests_utilities import RequestUtilities


class BasePage:
    """
    Parent class for page objects.
    """

    def __init__(
        self,
        browser: webdriver.Firefox | webdriver.Chrome,
        url: str,
        timeout: int = 5,
    ):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def is_element_present(self, how, what):
        """
        Check if an element is present on the page.
        """

        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def get_visible_element_text(self, how, what, timeout: int = 10):
        """
        Retrieve the text of a visible element on the page.
        """

        element = self.wait_for_element_ready((how, what), timeout=timeout)

        return element.text

    def get_visible_element_value(self, how, what, timeout: int = 10):
        """
        Retrieve the text of a visible element on the page.
        """

        element = self.wait_for_element_ready((how, what), timeout=timeout)

        return element.get_attribute("value")

    def get_list_of_elements_text(self, locator: tuple):
        """
        Retrieve the list of elements on the page.
        """

        rows = self.browser.find_elements(*locator)

        return [row.text for row in rows]

    def is_url_change(self, new_endpoint: str, timeout: int = 10):
        """
        Wait until the browser URL changes to include the specified new endpoint.
        """

        return WebDriverWait(self.browser, timeout).until(EC.url_to_be(new_endpoint))

    def open(self):
        """
        Open the web page using the specified URL.
        """

        self.browser.get(self.url)

    def is_element_not_attached(self, element):
        """
        Check an element is no longer attached to the DOM.
        """

        return WebDriverWait(self.browser, 5).until(EC.staleness_of(element))

    def is_element_visible_and_enabled(self, element):
        """
        Checks if an element is visible and enabled for interaction.
        """

        return (
            element.is_displayed() and element.is_enabled() and self.browser.execute_script(
                "return window.getComputedStyle(arguments[0]).visibility === 'visible';",
                element,
            )
        )

    def wait_for_element_ready(self, locator: tuple, timeout=10):
        """
        Waits for an element to become visible and enabled for interaction.
        """

        WebDriverWait(self.browser, timeout).until(
            lambda driver: self.is_element_visible_and_enabled(driver.find_element(*locator))
        )

        element = self.browser.find_element(*locator)

        logger.debug("Found element with name: %s", element.accessible_name)

        return element

    def send_text(self, locator: tuple, text: str, wait_timeout: float = 0):
        """
        Send text to element in form.
        """
        element = self.wait_for_element_ready(locator=locator)
        time.sleep(wait_timeout)
        element.clear()

        WebDriverWait(self.browser, 5).until(lambda _: element.get_attribute("value") == "")
        element.send_keys(text)
        logger.debug("Send keys: %s", element.accessible_name)

    def click_button(self, locator: tuple):
        """
        Click button in form.
        """
        element = self.wait_for_element_ready(locator=locator)
        element.click()
        logger.debug("Click element")

    def logout(self):
        """
        Click logout button.
        """
        logger.info("Logout.")
        self.click_button(locator=BasePageLocators.LOGOUT_BUTTON)

        base_url = RequestUtilities.get_base_url()
        self.is_url_change(base_url)
