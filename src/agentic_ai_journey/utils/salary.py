def filter_by_salary(employees, min_salary):
    """Return employees whose salary is at least min_salary."""
    return [emp for emp in employees if emp["salary"] >= min_salary]