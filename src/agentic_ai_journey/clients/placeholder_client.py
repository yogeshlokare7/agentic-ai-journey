import os
from types import TracebackType

import httpx

from agentic_ai_journey.models.placeholder import Post, User


class UserNotFoundError(Exception):
    def __init__(self, user_id: int) -> None:
        super().__init__(f"User {user_id} not found")
        self.user_id = user_id


class PlaceholderClient:
    def __init__(self, base_url: str | None = None, timeout: float = 10.0) -> None:
        base_url = base_url or os.getenv("API_BASE_URL")
        if not base_url:
            raise ValueError("API_BASE_URL is not set in the environment or .env file")
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def get_users(self) -> list[User]:
        response = self._client.get("/users")
        response.raise_for_status()
        return [User.model_validate(user) for user in response.json()]

    def get_user(self, user_id: int) -> User:
        response = self._client.get(f"/users/{user_id}")
        if response.status_code == httpx.codes.NOT_FOUND:
            raise UserNotFoundError(user_id)
        response.raise_for_status()
        return User.model_validate(response.json())

    def get_posts_by_user(self, user_id: int) -> list[Post]:
        response = self._client.get("/posts", params={"userId": user_id})
        response.raise_for_status()
        return [Post.model_validate(post) for post in response.json()]

    def create_post(self, user_id: int, title: str, body: str) -> Post:
        response = self._client.post(
            "/posts", json={"userId": user_id, "title": title, "body": body}
        )
        response.raise_for_status()
        return Post.model_validate(response.json())

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "PlaceholderClient":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()
