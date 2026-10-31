from agentic_ai_journey.models.employee import Employee


def filter_by_salary(employees: list[Employee], min_salary: int) -> list[str]:
    return [employee.name for employee in employees if employee.salary > min_salary]