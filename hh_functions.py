from itertools import count

import requests

from common_functions import predict_salary


def get_vacancies_hh(params: dict):
    url = 'https://api.hh.ru/vacancies'
    response = requests.get(url, params)
    response.raise_for_status()
    return response.json()


def predict_rub_salary_hh(vacancy):
    salary_details = vacancy['salary']
    if not salary_details:
        return None
    if salary_details['currency'] != 'RUR':
        return None
    return predict_salary(salary_details['from'], salary_details['to'])


def report_vacancies_hh(programming_languages, pages=5):
    if not pages:
        pages = float('inf')
    report = {'service': 'HeadHunter', 'city': 'Moscow'}
    report_languages = {}
    for language in programming_languages:
        vacancies = []
        for page in count(0):
            params = {'area': 1, 'text': language, 'page': page}
            page_vacancies = get_vacancies_hh(params)
            vacancies += page_vacancies['items']
            if page >= page_vacancies['pages'] or page >= pages:
                break
        language_salaries = []
        for vacancy in vacancies:
            salary = predict_rub_salary_hh(vacancy)
            if salary:
                language_salaries.append(salary)
        if language_salaries:
            average_salary = sum(language_salaries) // len(language_salaries)
        else:
            average_salary = 0
        language_details = {
            'vacancies_found': page_vacancies['found'],
            'vacancies_proccesed': len(language_salaries),
            'average_salary': average_salary
        }
        report_languages[language] = language_details
        report['items'] = report_languages
    return report
