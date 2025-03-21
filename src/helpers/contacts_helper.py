"""
This module provides utility functions for working with contacts.
"""

import logging as logger

from faker import Faker

from src.requests_utilities import RequestUtilities


class ContactsHelper:
    """
    Class with methods for contacts.
    """

    def __init__(self):
        self.request_utility = RequestUtilities()
        self.full_contact: int = 11

    @staticmethod
    def fake_contact():
        """
        Creates contact information using the Faker library.
        """

        logger.info("Create new contact.")
        fake = Faker()

        payload = {
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "birthdate": (
                fake.date_of_birth(minimum_age=6, maximum_age=110)
            ).strftime("%Y-%m-%d"),
            "email": fake.email(),
            "phone": fake.basic_phone_number(),
            "street1": fake.street_name(),
            "street2": fake.street_name(),
            "city": fake.city(),
            "stateProvince": fake.state(),
            "postalCode": fake.postalcode(),
            "country": fake.country()[:40],
        }

        logger.info("Fake contact created")

        return payload

    def create_contact(self):
        """
        Method for creating new contact.
        """

        payload = self.fake_contact()

        create_contact_json = self.request_utility.post(
            endpoint="contacts",
            payload=payload,
            expected_status_code=201,
        )

        return create_contact_json, payload

    def delete_contact(self, contact_id: str):
        """
        Method for deleting contact.
        """

        logger.info("Delete contact id=%s", contact_id)

        self.request_utility.delete(
            endpoint=f"contacts/{contact_id}",
        )

    def get_contacts(
        self,
        contact_id: str | None = None,
        expected_status_code: int = 200,
    ):
        """
        Method to get list of contacts.
        """

        if contact_id is None:
            logger.info("Get contacts")

            rs_get_contacts = self.request_utility.get(
                endpoint="contacts",
                expected_status_code=expected_status_code,
            )
            return rs_get_contacts

        logger.info("Get contact by id=%s", contact_id)

        rs_get_contact = self.request_utility.get(
            endpoint=f"contacts/{contact_id}",
            expected_status_code=expected_status_code,
        )
        return rs_get_contact

    def update(
        self,
        payload: dict,
        contact_id: str,
        expected_status_code: int = 200,
    ):
        """
        Method to update contact.
        """

        if len(payload) == self.full_contact:
            logger.info("Update contact with PUT.")

            rs_update_contact = self.request_utility.put(
                endpoint=f"contacts/{contact_id}",
                payload=payload,
                expected_status_code=expected_status_code,
            )
            return rs_update_contact

        if len(payload) < self.full_contact:
            logger.info("Update contact with PATCH.")

            rs_update_contact = self.request_utility.patch(
                endpoint=f"contacts/{contact_id}",
                payload=payload,
                expected_status_code=expected_status_code,
            )
            return rs_update_contact

        logger.info("Payload length does not match any expected condition.")
        return None
