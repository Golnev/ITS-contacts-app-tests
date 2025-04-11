"""
This module sets up configurations, fixtures, and helpers
for running Selenium-based and API-based tests with high level logic.
"""

import logging as logger
import os
import requests_cache

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from src.requests_utilities import RequestUtilities

load_dotenv()

base_url = RequestUtilities.get_base_url()


def pytest_addoption(parser):
    """
    Add custom command-line options for Pytest.

    Options:
    - `--rm`: Enables automatic deletion of created contacts after tests.
    - `--browser_name`: Specifies the browser to use (chrome or firefox).
    - `--docker`: Add argument for run tests in docker.
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
    parser.addoption(
        "--docker",
        action="store_true",
        default=False,
        help="Add arguments for docker.",
    )
    parser.addoption(
        "--logging_level",
        action="store",
        default="info",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "debug", "info", "warning", "error", "critical"],
        help="Custom logging level, (DEBUG, INFO).",
    )


def pytest_configure(config):
    custom_log_level = config.getoption("--logging_level")

    config.option.log_cli = True
    config.option.log_cli_level = custom_log_level.upper()

    loging_format = "%(asctime)s - %(levelname)s - %(message)s"
    config.option.log_cli_format = loging_format


@pytest.fixture
def browser(pytestconfig):
    """
    Initializes a Selenium WebDriver instance for the specified browser.
    """

    requests_cache.install_cache("webdriver_cache", expire_after=3600)

    browser_name = pytestconfig.getoption("--browser_name")

    docker_args = pytestconfig.getoption("--docker")

    if browser_name == "firefox":
        logger.info("Prepare browser firefox.")

        options = FirefoxOptions()

        service = FirefoxService(GeckoDriverManager().install())

        if docker_args:
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")

            service = FirefoxService(executable_path=GeckoDriverManager().install())

        firefox_path = os.getenv("FIREFOX_PATH")
        if firefox_path:
            options.binary_location = firefox_path

        driver = webdriver.Firefox(
            service=service,
            options=options,
        )

    elif browser_name == "chrome":
        logger.info("Prepare browser chrome.")

        if docker_args:
            options = ChromeOptions()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--remote-debugging-port=9222")

            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options,
            )

        else:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")

    yield driver

    logger.info("Browser quit.")
    if driver:
        driver.quit()
