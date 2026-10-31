import time

from dotenv import load_dotenv

from agentic_ai_journey.clients.placeholder_client import PlaceholderClient, UserNotFoundError

load_dotenv()

with PlaceholderClient() as client:
    start = time.perf_counter()
    for user in client.get_users():
        posts = client.get_posts_by_user(user.id)
        print(f"{user.name} | {user.company.name} | {len(posts)} posts")
    print(f"Took {time.perf_counter() - start:.2f}s")

    try:
        client.get_user(9999)
    except UserNotFoundError as e:
        print(f"Handled: {e}")
