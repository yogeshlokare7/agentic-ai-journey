import pytest
from pydantic import ValidationError

from agentic_ai_journey.models.placeholder import Post, User


@pytest.fixture
def user_data():
    return {
        "id": 1,
        "name": "Leanne Graham",
        "email": "Sincere@april.biz",
        "company": {
            "name": "Romaguera-Crona",
            "catchPhrase": "Multi-layered client-server neural-net",
            "bs": "harness real-time e-markets",
        },
    }


@pytest.fixture
def post_data():
    return {"id": 1, "userId": 1, "title": "Hello", "body": "First post"}


def test_valid_user_is_created(user_data):
    user = User(**user_data)

    assert user.name == "Leanne Graham"
    assert user.company.name == "Romaguera-Crona"


def test_user_ignores_extra_fields(user_data):
    user_data["phone"] = "1-770-736-8031"

    user = User(**user_data)

    assert not hasattr(user, "phone")


def test_user_without_company_raises_validation_error(user_data):
    del user_data["company"]

    with pytest.raises(ValidationError) as exc_info:
        User(**user_data)

    assert exc_info.value.errors()[0]["loc"] == ("company",)


def test_valid_post_is_created(post_data):
    post = Post(**post_data)

    assert post.user_id == 1
    assert post.title == "Hello"


def test_post_without_user_id_raises_validation_error(post_data):
    del post_data["userId"]

    with pytest.raises(ValidationError) as exc_info:
        Post(**post_data)

    assert exc_info.value.errors()[0]["loc"] == ("userId",)
    assert exc_info.value.errors()[0]["type"] == "missing"


def test_post_with_non_numeric_user_id_raises_validation_error(post_data):
    post_data["userId"] = "abc"

    with pytest.raises(ValidationError) as exc_info:
        Post(**post_data)

    assert exc_info.value.errors()[0]["loc"] == ("userId",)


def test_post_dumps_user_id_back_to_api_name(post_data):
    post = Post(**post_data)

    assert post.model_dump(by_alias=True)["userId"] == 1
    assert post.model_dump()["user_id"] == 1
