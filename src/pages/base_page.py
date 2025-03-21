"""
This module provides methods for interacting with the "Base" page.
"""

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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

    def get_visible_element(self, how, what, timeout: int = 10):
        """
        Retrieve a visible element on the page.
        """

        return WebDriverWait(self.browser, timeout).until(
            EC.visibility_of_element_located((how, what))
        )

    def get_visible_element_text(self, how, what, timeout: int = 10):
        """
        Retrieve the text of a visible element on the page.
        """

        return (
            WebDriverWait(self.browser, timeout)
            .until(EC.visibility_of_element_located((how, what)))
            .text
        )

    def get_clickable_element(self, how, what, timeout: int = 10):
        """
        Retrieve a clickable element on the page.
        """

        return WebDriverWait(self.browser, timeout).until(
            EC.element_to_be_clickable((how, what))
        )

    def open(self):
        """
        Open the web page using the specified URL.
        """

        self.browser.get(self.url)

    def is_element_visible_and_enabled(self, element):
        """
        Checks if an element is visible and enabled for interaction.
        """

        return (
            element.is_displayed()
            and element.is_enabled()
            and self.browser.execute_script(
                "return "
                "window.getComputedStyle(arguments[0])."
                "visibility === 'visible';",
                element,
            )
        )

    def wait_for_element_ready(self, locator, timeout=10):
        """
        Waits for an element to become visible and enabled for interaction.
        """

        WebDriverWait(self.browser, timeout).until(
            lambda driver: self.is_element_visible_and_enabled(
                driver.find_element(*locator)
            )
        )
        return self.browser.find_element(*locator)
