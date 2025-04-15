"""
This module provides a utility class for making HTTP requests.
"""

import logging as logger
import os
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

from src.helpers.auth_helper import with_auth_headers
from src.hosts_config import API_HOSTS

load_dotenv()


@dataclass
class RequestParams:
    """
    A data class representing parameters for an HTTP request.
    """

    endpoint: str
    payload: dict | None = None
    auth_extra: dict | None = None
    expected_status_code: int = 200


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
        self.url: str | None = None
        self.response_api = None
        self.EMPTY_CONTENT_LENGTH = "0"

    @staticmethod
    def assert_status_code(status_code, expected_status_code):
        """
        Validate the status code of the latest API response.
        """

        logger.info("Status code check.")
        assert status_code == expected_status_code, (
            f"Bad status code. "
            f"Expected status code: {expected_status_code}, "
            f"actual status code: {status_code}"
        )
        logger.info("Status is %s", status_code)

    def __make_request(
        self,
        method: str,
        request_params: RequestParams,
        auth_headers: dict | None = None,
    ):
        """
        Perform an HTTP request to the specified API endpoint.
        """

        logger.info("Starting %s method.", method.upper())

        if request_params.auth_extra and auth_headers:
            auth_headers.update(request_params.auth_extra)

        self.url = self.get_base_url() + request_params.endpoint
        logger.info("URL: %s", self.url)

        expected_status_code = request_params.expected_status_code

        self.response_api = requests.request(
            method=method,
            url=self.url,
            json=request_params.payload,
            headers=auth_headers,
            timeout=10,
        )

        status_code = self.response_api.status_code
        self.assert_status_code(status_code=status_code, expected_status_code=expected_status_code)

        if self.response_api.headers.get("Content-Length") == self.EMPTY_CONTENT_LENGTH:
            logger.info("Response has empty body (Content-Length: 0)")
            return None

        if method != "DELETE":
            response_json = self.response_api.json()
            logger.info("%s API response %s", method.upper(), response_json)
            return response_json

        return None

    @with_auth_headers
    def get(
        self,
        request_params: RequestParams,
        auth_headers=None,
    ):
        """
        Perform a GET request to the specified API endpoint.
        """

        return self.__make_request(
            method="GET",
            auth_headers=auth_headers,
            request_params=request_params,
        )

    @with_auth_headers
    def post(
        self,
        request_params: RequestParams,
        auth_headers=None,
    ):
        """
        Perform a POST request to the specified API endpoint.
        """
        return self.__make_request(
            method="POST",
            auth_headers=auth_headers,
            request_params=request_params,
        )

    @with_auth_headers
    def put(
        self,
        request_params: RequestParams,
        auth_headers=None,
    ):
        """
        Perform a PUT request to the specified API endpoint.
        """
        return self.__make_request(
            method="PUT",
            auth_headers=auth_headers,
            request_params=request_params,
        )

    @with_auth_headers
    def patch(
        self,
        request_params: RequestParams,
        auth_headers=None,
    ):
        """
        Perform a PATCH request to the specified API endpoint.
        """
        return self.__make_request(
            method="PATCH",
            auth_headers=auth_headers,
            request_params=request_params,
        )

    @with_auth_headers
    def delete(
        self,
        request_params: RequestParams,
        auth_headers=None,
    ):
        """
        Perform a DELETE request to the specified API endpoint.
        """
        return self.__make_request(
            method="DELETE",
            auth_headers=auth_headers,
            request_params=request_params,
        )
