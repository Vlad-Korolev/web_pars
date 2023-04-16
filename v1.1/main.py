# -*- coding: utf-8 -*-
# --- Встроенные модули.
from time import sleep
# --- Скаченные модули.
import requests
from bs4 import BeautifulSoup
# --- самописные модули.
from log import log
from sql import sql_insert
from bot import request_post


def get_soup(data):
    # Словарь для хранения всех найденных вакансий.
    vacancies_all = {}

    soup = BeautifulSoup(data, "html.parser")
    # print(soup.prettify()) # Вывод с отступами.

    match_all = soup.findAll('a', class_='vacancies__item-content')
    log(3, f"Всего найдено вакансий: {len(match_all)}", console=True, time=True)

    # Поиск совпадений, преобразования к нужному виду.
    for vacancie in match_all:
        category, title, city = (vacancie.getText('|', strip=True)).split('|')
        link = vacancie['href']

        # print("\n", vacancies[0].attrs) # Возможные атрибуты.
        # {'href': '/careers/all/vacancy/374/', 'class': ['vacancies__item-content'], 'style': 'display:none'}

        vacancie_content = {'category': str(category), 'title': str(title), 'city': str(city)}
        vacancies_all[link] = vacancie_content

    # В цикле проходим по каждой найденной вакансии.
    for key, value in vacancies_all.items():
        querry = f"""
                  INSERT INTO vacancie (category, city, title, link)
                  VALUES ('{value['category']}', '{value['city']}', '{value['title']}', 'https://selectel.ru{key}');
                  """
        log(2, f"Обрабатываем вакансию: https://selectel.ru{key})")
        # Запрос на запись информации о найденной вакансии в БД.
        # В случае успешной записи:
        if sql_insert(querry):
            s1 = "\n*[Новая вакансия]*\n"
            s2 = f"*Город:* {value['city']}\n"
            s3 = f"*Категория:* {value['category']}\n"
            s4 = f"*Наименование:* {value['title']}\n"
            s5 = f"*Ссылка:* https://selectel.ru/{key}"

            log(3, f"Новая вакансия добавлена в БД! ({value['title']}, https://selectel.ru{key})", console=True, time=True)
            request_post(s1+s2+s3+s4+s5)

        # В случае неудачной записи (уже имеется в БД):
        else:
            log(3, "Изменяем дату проверки вакансии в БД.")
            # Запрос на изменения (данная запис уже имеется в БД, меняем дату проверки).
            querry = f"""
                      UPDATE vacancie
                      SET check_date = CURRENT_TIMESTAMP
                      WHERE link = 'https://selectel.ru{key}';
                      """
            sql_insert(querry)


def get_page():

    url = "https://selectel.ru/careers/all/"
    log(3, f"Запрос по поиску новых вакансий: {url}")

    param = {'code': 'backend',
             'area': 'spb'}
    response = requests.get(url, params=param)

    if response.status_code == 200:
        log(3, f"Положительный ответ: {response.status_code}")
        get_soup(response.content.decode('utf-8'))

    else:
        log(2, f"Отрицательный ответ: {response.status_code}")


if __name__ == '__main__':
    log(3, f"Скрипт запущен, данные о работе записаны в лог-файл 'log/'", console = True)

    while True:
        try:
            log(3, f"Опрос сайта на наличие вакансий.", console = True, time = True)
            get_page()
            log(3, f"Режим ожидания (2 минуты).", console = True, time = True)
            sleep(120)
        except KeyboardInterrupt:
            log(2, f"Отмена выполнения.", console = True)
            quit()