# -*- coding: utf-8 -*-
# --- Встроенные модули.
import datetime
# --- Скаченные модули.
import requests
from bs4 import BeautifulSoup
# --- самописные модули.
from log import log
from sql import *

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
        vacancies_all[link] = vacancie_content
    
    for key, value in vacancies_all.items():
        # Получение текущей даты и времени.
        now = datetime.datetime.now()
        current_date = now.strftime("%d.%m.%Y_%H:%M") # ms: %S.%f

        querry = f"""
                  INSERT INTO vacancie (category, city, title, link, date)
                  VALUES ('{value['category']}', '{value['city']}', '{value['title']}', 'https://selectel.ru{key}', '{current_date}');

                 """
        if sql_insert(querry):
            print(f"\n[Вакансия]")
            print(f"Город:        {value['city']}")
            print(f"Категория:    {value['category']}")
            print(f"Наименование: {value['title']}")
            print(f"Ссылка:       https://selectel.ru/{key}")
            print(f"Добавлено в БД.")
            log(3, f"Добавлено в БД! (https://selectel.ru{key})")


        else:
            log(2, f"В Бд уже такая вакансия есть! (https://selectel.ru{key})")

            querry = f"""
                      UPDATE vacancie
                      SET check_date = '{current_date}'
                      WHERE link = 'https://selectel.ru{key}';
                      """
            sql_insert(querry)

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