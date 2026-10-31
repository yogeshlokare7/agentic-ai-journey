from agentic_ai_journey.utils.text import is_palindrome

def test_palindrome():
    assert is_palindrome("madam")
    assert not is_palindrome("hello")