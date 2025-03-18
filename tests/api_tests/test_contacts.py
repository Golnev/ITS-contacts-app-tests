"""
This module contains API tests for contacts management.
"""

# pylint: disable=unused-argument

import logging as logger
import pytest
from faker.proxy import Faker

from src.helpers.contacts_helper import ContactsHelper
from src.requests_utilities import RequestUtilities


pytestmark = pytest.mark.api


@pytest.mark.contacts
def test_add_contact(auth_headers, manage_contacts):
    """Test the addition of a new contact."""

    logger.info("TEST: Add new contact")

    contact_rs_api, contact_info = manage_contacts()

    assert contact_rs_api, "Request is empty"
    assert (
        contact_rs_api["lastName"] == contact_info["lastName"]
    ), "Last name from request nad from payload are different."


@pytest.mark.contacts
@pytest.mark.negative
def test_add_contact_without_mandatory_data(faker: Faker, auth_headers):
    """Test adding a contact without mandatory data (negative test case)."""

    logger.info("TEST: Add new contact without mandatory data.")

    payload = {
        "firstName": "",
        "lastName": "",
        "birthdate": (
            faker.date_of_birth(minimum_age=6, maximum_age=110)
        ).strftime("%Y-%m-%d"),
        "email": faker.email(),
        "phone": faker.basic_phone_number(),
        "street1": faker.street_name(),
        "street2": faker.street_name(),
        "city": faker.city(),
        "stateProvince": faker.state(),
        "postalCode": faker.postalcode(),
        "country": faker.country(),
    }

    request_utility = RequestUtilities()

    create_contact_json = request_utility.post(
        endpoint="contacts",
        payload=payload,
        headers=auth_headers,
        expected_status_code=400,
    )
    assert (
        create_contact_json is not None
    ), "Response is None, but expected JSON response."
    assert (
        create_contact_json["_message"] == "Contact validation failed"
    ), "Validation without mandatory data was successful."


@pytest.mark.contacts
@pytest.mark.negative
def test_contact_with_wrong_phone_number(faker: Faker, auth_headers):
    """Test adding a contact with an invalid phone number (negative test case)."""

    logger.info("TEST: Add new contact with wrong phone number.")

    payload = {
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "birthdate": (
            faker.date_of_birth(minimum_age=6, maximum_age=110)
        ).strftime("%Y-%m-%d"),
        "email": faker.email(),
        "phone": "No phone",
        "street1": faker.street_name(),
        "street2": faker.street_name(),
        "city": faker.city(),
        "stateProvince": faker.state(),
        "postalCode": faker.postalcode(),
        "country": faker.country(),
    }

    request_utility = RequestUtilities()

    create_contact_json = request_utility.post(
        endpoint="contacts",
        payload=payload,
        headers=auth_headers,
        expected_status_code=400,
    )
    assert (
        create_contact_json is not None
    ), "Response is None, but expected JSON response."

    assert (
        create_contact_json["message"]
        == "Contact validation failed: phone: Phone number is invalid"
    ), "Validation with string phone was successful."


@pytest.mark.contacts
@pytest.mark.negative
@pytest.mark.xfail
def test_add_contact_with_existing_last_name_and_first_name(
    faker: Faker, auth_headers, manage_contacts
):
    """Test adding a contact with an existing first and last name (negative test case)."""

    logger.info("TEST: Add contact with existing last name amd first name")

    contact_rs_api, _ = manage_contacts()

    payload = {
        "firstName": contact_rs_api["firstName"],
        "lastName": contact_rs_api["lastName"],
        "birthdate": (
            faker.date_of_birth(minimum_age=6, maximum_age=110)
        ).strftime("%Y-%m-%d"),
        "email": faker.email(),
        "phone": faker.basic_phone_number(),
        "street1": faker.street_name(),
        "street2": faker.street_name(),
        "city": faker.city(),
        "stateProvince": faker.state(),
        "postalCode": faker.postalcode(),
        "country": faker.country(),
    }

    request_utility = RequestUtilities()

    request_utility.post(
        endpoint="contacts",
        payload=payload,
        headers=auth_headers,
        expected_status_code=400,
    )


@pytest.mark.contacts
def test_get_contacts_list(auth_headers):
    """Test retrieving the list of all contacts."""

    logger.info("TEST: Get all contacts")

    contacts_helper = ContactsHelper()

    contacts = contacts_helper.get_contacts(auth_headers=auth_headers)

    assert contacts, "Contacts list is empty"


@pytest.mark.contacts
def test_get_contact(auth_headers, manage_contacts):
    """Test retrieving a specific contact by ID."""

    logger.info("TEST: Get contact")

    contact_rs_api, _ = manage_contacts()
    contact_id = contact_rs_api["_id"]

    contacts_helper = ContactsHelper()
    contact = contacts_helper.get_contacts(
        auth_headers=auth_headers, contact_id=contact_id
    )

    assert (
        contact_rs_api is not None and contact is not None
    ), "Response is None, but expected JSON response."
    assert contact_rs_api["lastName"] == contact["lastName"]


@pytest.mark.contacts
@pytest.mark.negative
def test_get_not_existing_contact(auth_headers, manage_contacts):
    """Test retrieving a non-existent contact (negative test case)."""

    logger.info("TEST: Get nonexistent contact")

    contact_rs_api, _ = manage_contacts()
    contact_id = contact_rs_api["_id"]

    contacts_helper = ContactsHelper()
    contacts_helper.delete_contact(
        auth_headers=auth_headers, contact_id=contact_id
    )

    deleted_contact = contacts_helper.get_contacts(
        auth_headers=auth_headers,
        contact_id=contact_id,
        expected_status_code=404,
    )

    assert not deleted_contact, "Request is not empty."


@pytest.mark.contacts
def test_update_contact(faker: Faker, auth_headers, manage_contacts):
    """Test updating a contact's details."""

    logger.info("TEST: Full update contact.")

    contact_rs_api, _ = manage_contacts()

    contact_id = contact_rs_api["_id"]

    payload = {
        "firstName": contact_rs_api["firstName"],
        "lastName": contact_rs_api["lastName"],
        "birthdate": contact_rs_api["birthdate"],
        "email": contact_rs_api["email"],
        "phone": faker.basic_phone_number(),
        "street1": contact_rs_api["street1"],
        "street2": faker.street_name(),
        "city": contact_rs_api["city"],
        "stateProvince": contact_rs_api["stateProvince"],
        "postalCode": faker.postalcode(),
        "country": contact_rs_api["country"],
    }

    logger.info(
        "Update contact with id=%s, "
        "Update phone=%s, Update street2=%s, "
        "Update postalCode=%s.",
        contact_id,
        payload["phone"],
        payload["street2"],
        payload["postalCode"],
    )

    contacts_helper = ContactsHelper()
    update_contact = contacts_helper.update(
        auth_headers=auth_headers, payload=payload, contact_id=contact_id
    )
    assert (
        update_contact is not None
    ), "Response is None, but expected JSON response."

    assert contact_id == update_contact["_id"]
    assert payload["phone"] == update_contact["phone"]
    assert payload["street2"] == update_contact["street2"]
    assert payload["postalCode"] == update_contact["postalCode"]


@pytest.mark.contacts
@pytest.mark.negative
def test_update_not_existing_contact(
    faker: Faker, auth_headers, manage_contacts
):
    """Test updating a contact that does not exist (negative test case)."""

    logger.info("TEST: Update not existing contact")

    contact_rs_api, _ = manage_contacts()
    contact_id = contact_rs_api["_id"]

    contacts_helper = ContactsHelper()
    contacts_helper.delete_contact(
        auth_headers=auth_headers, contact_id=contact_id
    )

    payload = {
        "firstName": contact_rs_api["firstName"],
        "lastName": contact_rs_api["lastName"],
        "birthdate": contact_rs_api["birthdate"],
        "email": contact_rs_api["email"],
        "phone": faker.basic_phone_number(),
        "street1": contact_rs_api["street1"],
        "street2": faker.street_name(),
        "city": contact_rs_api["city"],
        "stateProvince": contact_rs_api["stateProvince"],
        "postalCode": faker.postalcode(),
        "country": contact_rs_api["country"],
    }

    logger.info(
        "Update contact with id=%s, Update phone=%s, Update street2=%s, Update postalCode=%s.",
        contact_id,
        payload["phone"],
        payload["street2"],
        payload["postalCode"],
    )

    contacts_helper = ContactsHelper()
    update_contact = contacts_helper.update(
        auth_headers=auth_headers,
        payload=payload,
        contact_id=contact_id,
        expected_status_code=404,
    )

    assert not update_contact, "Request is not empty."


@pytest.mark.contacts
@pytest.mark.negative
def test_update_contact_with_wrong_data(auth_headers, manage_contacts):
    """Test updating a contact with invalid data (negative test case)."""

    logger.info("TEST: Update not existing contact")

    contact_rs_api, _ = manage_contacts()
    contact_id = contact_rs_api["_id"]

    contacts_helper = ContactsHelper()
    contacts_helper.delete_contact(
        auth_headers=auth_headers, contact_id=contact_id
    )

    payload = {
        "firstName": contact_rs_api["firstName"],
        "lastName": contact_rs_api["lastName"],
        "birthdate": contact_rs_api["birthdate"],
        "email": contact_rs_api["email"],
        "phone": "No Phone number",
        "street1": contact_rs_api["street1"],
        "street2": contact_rs_api["street2"],
        "city": contact_rs_api["city"],
        "stateProvince": contact_rs_api["stateProvince"],
        "postalCode": "No postal code",
        "country": contact_rs_api["country"],
    }

    logger.info(
        "Update contact with id=%s, Update phone=%s, Update street2=%s, Update postalCode=%s.",
        contact_id,
        payload["phone"],
        payload["street2"],
        payload["postalCode"],
    )

    contacts_helper = ContactsHelper()
    update_contact = contacts_helper.update(
        auth_headers=auth_headers,
        payload=payload,
        contact_id=contact_id,
        expected_status_code=400,
    )

    assert (
        update_contact is not None
    ), "Response is None, but expected JSON response."

    assert (
        update_contact["message"] == "Validation failed: "
        "postalCode: "
        "Path `postalCode` (`No postal code`) is "
        "longer than the maximum allowed length (10)., "
        "phone: Phone number is invalid"
    ), "Validation with wrong 'postal code' and 'phone' was successfully"


@pytest.mark.contacts
def test_update_last_name_contact(faker: Faker, auth_headers, manage_contacts):
    """Test updating the last name of a contact."""

    logger.info("TEST: Update last name contact")

    contact_rs_api, _ = manage_contacts()
    contact_id = contact_rs_api["_id"]

    update_lastname = faker.last_name()
    payload = {"lastName": update_lastname}

    contacts_helper = ContactsHelper()
    update_contact = contacts_helper.update(
        auth_headers=auth_headers,
        payload=payload,
        contact_id=contact_id,
    )
    assert (
        update_contact is not None
    ), "Response is None, but expected JSON response."

    assert update_contact["_id"] == contact_id, (
        f"Expected contact ID to be {contact_id}, "
        f"but got {update_contact['_id']}"
    )

    assert update_contact["lastName"] == update_lastname, (
        f"Expected last name to be {update_lastname}, "
        f"but got {update_contact['lastName']}"
    )


@pytest.mark.contacts
def test_update_email_contact(faker: Faker, auth_headers, manage_contacts):
    """Test updating the email address of a contact."""

    logger.info("TEST: Update email contact")

    contact_rs_api, _ = manage_contacts()
    contact_id = contact_rs_api["_id"]

    update_email = faker.email()
    payload = {"email": update_email}

    contacts_helper = ContactsHelper()
    update_contact = contacts_helper.update(
        auth_headers=auth_headers,
        payload=payload,
        contact_id=contact_id,
    )
    assert (
        update_contact is not None
    ), "Response is None, but expected JSON response."

    assert update_contact["_id"] == contact_id, (
        f"Expected contact ID to be {contact_id}, "
        f"but got {update_contact['_id']}"
    )

    assert update_contact["email"] == update_email, (
        f"Expected email to be {update_email}, "
        f"but got {update_contact['email']}"
    )


@pytest.mark.contacts
def test_upgrade_first_name_and_postal_code_together(
    faker: Faker, auth_headers, manage_contacts
):
    """Test updating the first name and postal code of a contact simultaneously."""

    logger.info("TEST: Update first name and postal code contact")

    contact_rs_api, _ = manage_contacts()
    contact_id = contact_rs_api["_id"]

    update_firstname = faker.first_name()
    update_postal_code = faker.postalcode()
    payload = {"firstName": update_firstname, "postalCode": update_postal_code}

    contacts_helper = ContactsHelper()
    update_contact = contacts_helper.update(
        auth_headers=auth_headers,
        payload=payload,
        contact_id=contact_id,
    )
    assert (
        update_contact is not None
    ), "Response is None, but expected JSON response."

    assert update_contact["_id"] == contact_id, (
        f"Expected contact ID to be {contact_id}, "
        f"but got {update_contact['_id']}"
    )

    assert update_contact["firstName"] == update_firstname, (
        f"Expected email to be {update_firstname}, "
        f"but got {update_contact["firstName"]}"
    )

    assert update_contact["postalCode"] == update_postal_code, (
        f"Expected email to be {update_postal_code}, "
        f"but got {update_contact['postalCode']}"
    )


@pytest.mark.contacts
@pytest.mark.negative
@pytest.mark.parametrize("phone", ["No Phone", 12345678901234567890])
def test_update_phone_with_wrong_data(auth_headers, manage_contacts, phone):
    """Test updating a contact with an invalid phone number (negative test case)."""

    logger.info("TEST: Update contact phone number with wrong data.")

    contact_rs_api, _ = manage_contacts()
    contact_id = contact_rs_api["_id"]

    payload = {"phone": phone}

    contacts_helper = ContactsHelper()
    update_contact = contacts_helper.update(
        auth_headers=auth_headers,
        payload=payload,
        contact_id=contact_id,
        expected_status_code=400,
    )

    assert (
        update_contact is not None
    ), "Response is None, but expected JSON response."

    assert (
        update_contact["_message"] == "Contact validation failed"
    ), f"Update contact with wrong phone number={phone}"
