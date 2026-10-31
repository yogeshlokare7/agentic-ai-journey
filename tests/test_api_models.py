import pytest
from pydantic import ValidationError

from agentic_ai_journey.models.api_models import Customer


@pytest.fixture
def customer_data():
    return {
        "name": "Asha Patil",
        "age": 29,
        "email": "asha.patil@example.com",
        "address": {"city": "Pune", "pincode": "411001"},
        "tags": ["premium"],
    }


def test_valid_customer_is_created(customer_data):
    customer = Customer(**customer_data)

    assert customer.name == "Asha Patil"
    assert customer.address.pincode == "411001"


def test_non_numeric_pincode_raises_validation_error(customer_data):
    customer_data["address"]["pincode"] = "42200A"

    with pytest.raises(ValidationError) as exc_info:
        Customer(**customer_data)

    assert exc_info.value.errors()[0]["loc"] == ("address", "pincode")


def test_underage_customer_raises_validation_error(customer_data):
    customer_data["age"] = 15

    with pytest.raises(ValidationError) as exc_info:
        Customer(**customer_data)

    assert exc_info.value.errors()[0]["loc"] == ("age",)


def test_missing_name_raises_validation_error(customer_data):
    del customer_data["name"]

    with pytest.raises(ValidationError) as exc_info:
        Customer(**customer_data)

    assert exc_info.value.errors()[0]["type"] == "missing"


def test_email_without_at_sign_raises_validation_error(customer_data):
    customer_data["email"] = "asha.example.com"

    with pytest.raises(ValidationError) as exc_info:
        Customer(**customer_data)

    assert exc_info.value.errors()[0]["loc"] == ("email",)
