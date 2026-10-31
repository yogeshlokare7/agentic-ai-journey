from collections import Counter

def count_words(text: str) -> Counter[str]:
    words = (w.strip(".,!?;:\"'()") for w in text.lower().split())
    return Counter(w for w in words if w)

def is_palindrome(text: str) -> bool:
    cleaned = "".join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]