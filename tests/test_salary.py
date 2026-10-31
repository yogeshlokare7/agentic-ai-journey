from agentic_ai_journey.models.employee import Employee
from agentic_ai_journey.utils.salary import filter_by_salary


def test_filter_by_salary_returns_names_of_employees_above_min_salary():
	employees : list[Employee] = [
		Employee("Alice", 50_000),
		Employee("Bob", 75_000),
		Employee("Cara", 100_000),
	]

	assert filter_by_salary(employees, 75_000) == ["Cara"]
