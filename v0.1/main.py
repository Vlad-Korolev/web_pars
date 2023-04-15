# -*- coding: utf-8 -*-
# --- Встроенные модули.
# --- Скаченные модули.
import requests
from bs4 import BeautifulSoup
# --- самописные модули.
from log import log

vacancies_all = {}

def get_soup(data):
    soup = BeautifulSoup(data, "html.parser")
    # print(soup.prettify()) # Вывод с отступами.

    match_all = soup.findAll('a', class_='vacancies__item-content')
    log(3, f"Всего найдено совпадений по вакансиям: {len(match_all)}")

    for vacancie in match_all:
        category, title, city = (vacancie.getText('|', strip = True)).split('|')
        link = vacancie['href']

        # print("\n", vacancies[0].attrs) # Возможные атрибуты.
        # {'href': '/careers/all/vacancy/374/', 'class': ['vacancies__item-content'], 'style': 'display:none'}

        vacancie_content = {'category': str(category), 'title': str(title), 'city': str(city)}
        print(vacancie_content)
        vacancies_all[link] = vacancie_content
    
    for key, value in vacancies_all.items():
        print(f"\n[Вакансия]")
        print(f"Город:        {value['city']}")
        print(f"Категория:    {value['category']}")
        print(f"Наименование: {value['title']}")
        print(f"Ссылка:       https://selectel.ru/{key}")

def get_page():
    url = "https://selectel.ru/careers/all/"

    param = {'code': 'backend', 
             'area': 'spb'}
      
    response = requests.get(url, params = param)
    if response.status_code == 200:
        log(3, f"Положительный ответ от сайта: {response.status_code}")
        get_soup(response.content.decode('utf-8'))
    else:
        log(2, f"Отрицательный ответ от сайта: {response.status_code}")

def main():
    get_page()

if __name__ == '__main__':
    main()