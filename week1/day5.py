from agentic_ai_journey.clients.placeholder_client import PlaceholderClient, UserNotFoundError

with PlaceholderClient() as client:
    for user in client.get_users():
        posts = client.get_posts_by_user(user.id)
        print(f"{user.name} | {user.company.name} | {len(posts)} posts")

    try:
        client.get_user(9999)
    except UserNotFoundError as e:
        print(f"Handled: {e}")
