import os

from dotenv import load_dotenv

from common_functions import draw_terminal_table
from hh_functions import report_vacancies_hh
from sj_functions import report_vacancies_sj

PROGRAMMING_LANGUAGES = ['Python', 'Java']


def main():
    load_dotenv()
    sj_api_token = os.getenv('SJ_API_TOKEN')
    vacancies_hh = report_vacancies_hh(PROGRAMMING_LANGUAGES)
    vacancies_sj = report_vacancies_sj(PROGRAMMING_LANGUAGES, SJ_API_TOKEN)
    draw_terminal_table(vacancies_hh)
    draw_terminal_table(vacancies_sj)


if __name__ == '__main__':
    main()
