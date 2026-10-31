import asyncio
import json

import httpx
import pytest
import pytest_asyncio
import respx

from agentic_ai_journey.clients.async_placeholder_client import AsyncPlaceholderClient
from agentic_ai_journey.clients.placeholder_client import UserNotFoundError

BASE_URL = "https://api.test"

USER = {
    "id": 1,
    "name": "Leanne Graham",
    "email": "Sincere@april.biz",
    "company": {"name": "Romaguera-Crona"},
}
POST = {"id": 1, "userId": 1, "title": "Hello", "body": "First post"}


@pytest_asyncio.fixture
async def client():
    async with AsyncPlaceholderClient(base_url=BASE_URL) as c:
        yield c


@pytest.fixture
def api():
    with respx.mock(base_url=BASE_URL, assert_all_called=True) as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_users_returns_user_models(client, api):
    api.get("/users").respond(json=[USER])

    users = await client.get_users()

    assert len(users) == 1
    assert users[0].company.name == "Romaguera-Crona"


@pytest.mark.asyncio
async def test_get_user_returns_user(client, api):
    api.get("/users/1").respond(json=USER)

    user = await client.get_user(1)

    assert user.name == "Leanne Graham"


@pytest.mark.asyncio
async def test_get_user_raises_not_found_on_404(client, api):
    api.get("/users/9999").respond(404, json={})

    with pytest.raises(UserNotFoundError) as exc_info:
        await client.get_user(9999)

    assert exc_info.value.user_id == 9999


@pytest.mark.asyncio
async def test_server_error_raises_http_status_error(client, api):
    api.get("/users/1").respond(500)

    with pytest.raises(httpx.HTTPStatusError):
        await client.get_user(1)


@pytest.mark.asyncio
async def test_get_posts_by_user_sends_user_id_param(client, api):
    route = api.get("/posts", params={"userId": "1"}).respond(json=[POST, POST])

    posts = await client.get_posts_by_user(1)

    assert len(posts) == 2
    assert route.called


@pytest.mark.asyncio
async def test_create_post_sends_json_body(client, api):
    route = api.post("/posts").respond(201, json={**POST, "id": 101})

    post = await client.create_post(1, "Hello", "First post")

    assert post.id == 101
    sent = json.loads(route.calls.last.request.content)
    assert sent == {"userId": 1, "title": "Hello", "body": "First post"}


@pytest.mark.asyncio
async def test_gather_with_return_exceptions_keeps_other_results(client, api):
    api.get("/users/1").respond(json=USER)
    api.get("/users/2").respond(json={**USER, "id": 2, "name": "Ervin Howell"})
    api.get("/users/9999").respond(404, json={})

    results = await asyncio.gather(
        client.get_user(1), client.get_user(9999), client.get_user(2), return_exceptions=True
    )

    assert results[0].name == "Leanne Graham"
    assert isinstance(results[1], UserNotFoundError)
    assert results[2].name == "Ervin Howell"


def test_missing_base_url_raises(monkeypatch):
    monkeypatch.delenv("API_BASE_URL", raising=False)

    with pytest.raises(ValueError):
        AsyncPlaceholderClient()
