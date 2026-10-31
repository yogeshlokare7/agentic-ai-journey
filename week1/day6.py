import asyncio
import time

from dotenv import load_dotenv

from agentic_ai_journey.clients.async_placeholder_client import AsyncPlaceholderClient
from agentic_ai_journey.models.placeholder import Post, User


async def report(client: AsyncPlaceholderClient) -> list[User]:
    start = time.perf_counter()

    users = await client.get_users()
    all_posts = await asyncio.gather(*(client.get_posts_by_user(user.id) for user in users))

    for user, posts in zip(users, all_posts):
        print(f"{user.name} | {user.company.name} | {len(posts)} posts")

    print(f"Took {time.perf_counter() - start:.2f}s")
    return users


async def partial_failure(client: AsyncPlaceholderClient) -> None:
    user_ids = [1, 2, 9999, 3]
    results = await asyncio.gather(
        *(client.get_user(user_id) for user_id in user_ids), return_exceptions=True
    )

    for user_id, result in zip(user_ids, results):
        if isinstance(result, BaseException):
            print(f"User {user_id}: ERROR {result}")
        else:
            print(f"User {user_id}: {result.name}")


async def rate_limited(client: AsyncPlaceholderClient, users: list[User]) -> None:
    semaphore = asyncio.Semaphore(3)
    running = 0

    async def fetch(user_id: int) -> list[Post]:
        nonlocal running
        async with semaphore:
            running += 1
            print(f"start user {user_id:>2} (running: {running})")
            posts = await client.get_posts_by_user(user_id)
            running -= 1
            print(f"end   user {user_id:>2} (running: {running})")
            return posts

    all_posts = await asyncio.gather(*(fetch(user.id) for user in users))
    print(f"Fetched {sum(len(posts) for posts in all_posts)} posts")


async def main() -> None:
    async with AsyncPlaceholderClient() as client:
        print("== Report ==")
        users = await report(client)

        print("\n== Partial failure ==")
        await partial_failure(client)

        print("\n== Rate limit: Semaphore(3) ==")
        await rate_limited(client, users)


load_dotenv()
asyncio.run(main())
