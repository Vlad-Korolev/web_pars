# web_pars
[Описание проекта]
Небольшоой web-парсер, способен собирать веб-данные о вакансиях на сайте Selectel, хранит информацию в БД (SQLite), переодически опрашивая сайт, при нахождении новых отправляет уведомленияв Телеграмм, ведет подробный лог-файл работы.

[Краткое описание версий]
v1.1 - Мелкие исправления кода.
v1.0 - Улучшена работа с БД, логирования, отправки уведомлений в Телеграмм.
v0.3 - Улучшена работа с БД (выявления уже добавленных вакансий  и т.п.). Добавлена возможнсть отправки уведомлений о новых вакансиях в Телеграмм.
v0.2 - Добавлена возможность работы с БД, хранения записей о вакансиях (SQLite).
v0.1 - Парсер способен обрабатывать запросы и искать нужное на стринце (выводит в консоль). Добавлена возможность ведения лог-файла выполнения.

[requirements.txt]
requests==2.28.2
beautifulsoup4==4.12.2


