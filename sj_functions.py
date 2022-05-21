import requests
from itertools import count

from common_functions import predict_salary


def get_vacancies_sj(params, sj_token):
    url = 'https://api.superjob.ru/2.0/vacancies'
    headers = {'X-Api-App-Id': sj_token}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def predict_rub_salary_sj(vacancy):
    if vacancy['currency'] != 'rub':
        return None
    return predict_salary(vacancy['payment_from'], vacancy['payment_to'])


def report_vacancies_sj(programming_languages, sj_token, pages=5):
    if not pages:
        pages = float('inf')
    report = {'service': 'Superjob', 'city': 'Moscow'}
    report_languages = {}
    for language in programming_languages:
        vacancies = []
        for page in count(0):
            params = {'keyword': language, 'town': 4,
                      'catalogues': 48, 'page': page}
            page_vacancies = get_vacancies_sj(params, sj_token)
            vacancies += page_vacancies['objects']
            if page >= page_vacancies['total'] // 20 or page >= pages:
                break
        language_salaries = []
        for vacancy in vacancies:
            salary = predict_rub_salary_sj(vacancy)
            if salary:
                language_salaries.append(salary)
        if language_salaries:
            average_salary = sum(language_salaries) // len(language_salaries)
        else:
            average_salary = 0
        language_details = {
            'vacancies_found': page_vacancies['total'],
            'vacancies_proccesed': len(language_salaries),
            'average_salary': average_salary}
        report_languages[language] = language_details
        report['items'] = report_languages
    return report
