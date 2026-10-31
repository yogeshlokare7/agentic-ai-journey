from agentic_ai_journey.utils.salary import filter_by_salary


def test_filter_by_salary_returns_names_of_employees_above_min_salary():
	employees = [
		{"name": "Alice", "salary": 50_000},
		{"name": "Bob", "salary": 75_000},
		{"name": "Cara", "salary": 100_000},
	]

	assert filter_by_salary(employees, 75_000) == ["Cara"]
