def filter_by_salary(employees: list[dict[str, int | str]], min_salary: int) -> list[str]:
    return [str(e["name"]) for e in employees if int(e["salary"]) > min_salary]