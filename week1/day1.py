print("Hello from Day1!")


# 1. Word count
def count_words(text):
    """Return total word count and frequency of each word."""
    words = text.lower().split()
    freq = {}
    for word in words:
        word = word.strip(".,!?;:\"'()")
        if word:
            freq[word] = freq.get(word, 0) + 1
    return sum(freq.values()), freq


# 2. Salary filter
employees = [
    {"name": "Amit", "salary": 45000},
    {"name": "Priya", "salary": 72000},
    {"name": "Rahul", "salary": 58000},
    {"name": "Sneha", "salary": 91000},
    {"name": "Vikram", "salary": 38000},
]


def filter_by_salary(employees, min_salary):
    """Return employees whose salary is at least min_salary."""
    return [emp for emp in employees if emp["salary"] >= min_salary]


# 3. Palindrome check
def is_palindrome(text):
    """Check palindrome, ignoring case, spaces and punctuation."""
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]


if __name__ == "__main__":
    sentence = "The quick brown fox jumps over the lazy dog. The dog sleeps."
    total, freq = count_words(sentence)
    print(f"\nTotal words: {total}")
    print(f"Word frequency: {freq}")

    print("\nEmployees with salary >= 50000:")
    for emp in filter_by_salary(employees, 50000):
        print(f"  {emp['name']}: {emp['salary']}")

    print("\nPalindrome check:")
    for word in ["madam", "racecar", "hello", "A man, a plan, a canal: Panama"]:
        print(f"  {word!r} -> {is_palindrome(word)}")
