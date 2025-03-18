"""
This module provides a utility class for making HTTP requests.
"""

import logging as logger
import os

import requests
from dotenv import load_dotenv

from src.hosts_config import API_HOSTS

load_dotenv()


# pylint: disable=too-many-instance-attributes
class RequestUtilities:
    """
    A utility class for sending HTTP requests and handling API responses.
    """

    @staticmethod
    def get_base_url():
        """
        Retrieve the base URL for API requests based on the environment.
        """

        env = os.getenv("ENV", "test")
        base_url = API_HOSTS[env]
        return base_url

    def __init__(self):
        self.__env = os.getenv("ENV", "test")
        self.base_url: str = API_HOSTS[self.__env]

        self.status_code: int | None = None
        self.expected_status_code: int | None = None
        self.url: str | None = None

        self.response_api = None
        self.response_json = None

        self.EMPTY_CONTENT_LENGTH = "0"  # pylint: disable=invalid-name

    def __assert_status_code(self):
        """
        Validate the status code of the latest API response.
        """

        logger.info("Status code check.")
        assert self.status_code == self.expected_status_code, (
            f"Bad status code. "
            f"Expected status code: {self.expected_status_code}, "
            f"actual status code: {self.status_code}"
        )
        logger.info("Status is %s", self.status_code)

    def get(
        self,
        endpoint: str,
        headers: dict | None = None,
        expected_status_code=200,
    ):
        """
        Perform a GET request to the specified API endpoint.
        """

        logger.info("Starting GET method.")

        if not headers:
            headers = {"Content-Type": "application/json"}
        else:
            headers.update({"Content-Type": "application/json"})

        self.url = self.base_url + endpoint
        logger.info("URL: %s", self.url)

        self.expected_status_code = expected_status_code

        self.response_api = requests.get(
            url=self.url,
            headers=headers,
            timeout=5,
        )
        self.status_code = self.response_api.status_code
        self.__assert_status_code()

        if (
            self.response_api.headers.get("Content-Length")
            == self.EMPTY_CONTENT_LENGTH
        ):
            logger.info("Response has empty body (Content-Length: 0)")
            return None

        self.response_json = self.response_api.json()

        logger.info("GET API response %s", self.response_json)

        return self.response_json

    def post(
        self,
        endpoint: str,
        payload: dict | None = None,
        headers: dict | None = None,
        expected_status_code=200,
    ):
        """
        Perform a POST request to the specified API endpoint.
        """

        logger.info("Starting POST method.")

        if not headers:
            headers = {"Content-Type": "application/json"}
        else:
            headers.update({"Content-Type": "application/json"})

        self.url = self.base_url + endpoint
        logger.info("URL: %s", self.url)

        self.expected_status_code = expected_status_code

        self.response_api = requests.post(
            url=self.url,
            json=payload,
            headers=headers,
            timeout=10,
        )

        self.status_code = self.response_api.status_code

        self.__assert_status_code()

        if (
            self.response_api.headers.get("Content-Length")
            == self.EMPTY_CONTENT_LENGTH
        ):
            logger.info("Response has empty body (Content-Length: 0)")
            return None

        if payload is None:
            return None

        self.response_json = self.response_api.json()

        logger.info("POST API response %s", self.response_json)

        return self.response_json

    def put(
        self,
        endpoint: str,
        payload: dict | None = None,
        headers: dict | None = None,
        expected_status_code=200,
    ):
        """
        Perform a PUT request to the specified API endpoint.
        """

        logger.info("Starting PUT method.")

        if not headers:
            headers = {"Content-Type": "application/json"}
        else:
            headers.update({"Content-Type": "application/json"})

        self.url = self.base_url + endpoint
        logger.info("URL: %s", self.url)

        self.expected_status_code = expected_status_code

        self.response_api = requests.put(
            url=self.url,
            json=payload,
            headers=headers,
            timeout=10,
        )

        self.status_code = self.response_api.status_code

        self.__assert_status_code()

        if (
            self.response_api.headers.get("Content-Length")
            == self.EMPTY_CONTENT_LENGTH
        ):
            logger.info("Response has empty body (Content-Length: 0)")
            return None

        if payload is None:
            return None

        self.response_json = self.response_api.json()

        logger.info("PUT API response %s", self.response_json)

        return self.response_json

    def patch(
        self,
        endpoint: str,
        payload: dict | None = None,
        headers: dict | None = None,
        expected_status_code=200,
    ):
        """
        Perform a PATCH request to the specified API endpoint.
        """

        logger.info("Starting PATCH method.")

        if not headers:
            headers = {"Content-Type": "application/json"}
        else:
            headers.update({"Content-Type": "application/json"})

        self.url = self.base_url + endpoint
        logger.info("URL: %s", self.url)

        self.expected_status_code = expected_status_code

        self.response_api = requests.patch(
            url=self.url,
            json=payload,
            headers=headers,
            timeout=10,
        )

        self.status_code = self.response_api.status_code

        self.__assert_status_code()

        if (
            self.response_api.headers.get("Content-Length")
            == self.EMPTY_CONTENT_LENGTH
        ):
            logger.info("Response has empty body (Content-Length: 0)")
            return None

        if payload is None:
            return None

        self.response_json = self.response_api.json()

        logger.info("PATCH API response %s", self.response_json)

        return self.response_json

    def delete(
        self,
        endpoint: str,
        headers: dict | None = None,
        expected_status_code=200,
    ):
        """
        Perform a DELETE request to the specified API endpoint.
        """

        logger.info("Starting DELETE method.")

        if not headers:
            headers = {"Content-Type": "application/json"}

        self.url = self.base_url + endpoint
        logger.info("URL: %s", self.url)

        self.expected_status_code = expected_status_code

        self.response_api = requests.delete(
            url=self.url,
            headers=headers,
            timeout=10,
        )
        self.status_code = self.response_api.status_code
        self.__assert_status_code()
