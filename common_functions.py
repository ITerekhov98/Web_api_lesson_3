from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    if all([salary_from, salary_to]):
        return int((salary_from + salary_to) // 2)
    elif salary_from:
        return int(salary_from * 1.2)
    elif salary_to:
        return int(salary_to * 0.8)


def draw_terminal_table(report_vacancies: dict):
    serialised_data = [['Язык программирования', 'Вакансий найдено',
                       'Вакансий обработано', 'Средняя зарплата']]
    for language, details in report_vacancies['items'].items():
        serialised_data.append((language, *details.values()))
    table = AsciiTable(serialised_data)
    table.title = f"{report_vacancies['service']} {report_vacancies['city']}"
    print(table.table)
