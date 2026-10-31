from agentic_ai_journey.utils.text import count_words, is_palindrome


def test_count_words():
    assert count_words("Hello, hello world!") == {"hello": 2, "world": 1}

def test_palindrome():
    assert is_palindrome("madam")
    assert not is_palindrome("hello")