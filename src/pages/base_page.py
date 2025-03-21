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

    def get_visible_element(self, how, what, timeout: int = 5):
        """
        Retrieve the text of a visible element on the page.
        """

        return (
            WebDriverWait(self.browser, timeout)
            .until(EC.visibility_of_element_located((how, what)))
            .text
        )

    def open(self):
        """
        Open the web page using the specified URL.
        """

        self.browser.get(self.url)
