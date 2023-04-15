# --- Встроенные модули.
import sqlite3
import json
# --- Скаченные модули.
import requests
# --- самописные модули.
from log import log
from sql import *


def request_post(text: str):
    '''
    Функция 'request_post(req_url, req_param)', отправляет post-запросы на сервер.
        В качестве аргументов ожидает:
        "text" - текст сообщения.
    Функция ничего не возвращает.
    '''

    log(3, f'Запрос jотправку сообщения в Телеграмм.')
    
    token = sql_select("SELECT token FROM bot WHERE name = '@Vlad_Korolev_bot'")[0][0]
    chats = sql_select("SELECT chat_id FROM bot_chat")
    url =  f"https://api.telegram.org/bot{token}/sendMessage"

    log(3, f'Чатов для отправки: {len(chats)}')
    for chat in chats:
        
        log(3, f'Отправка POST-запроса в чат: {chat[0]}')
        # Обрабатываем отправку POST-запроса (отправляется в json формате).
        try:
            param = {'chat_id'      : chat[0], 
                        'parse_mode': 'markdown',
                        'text'      : text}
            
            response = requests.post(url, data = param).json()
            log(3, f'Запрос POST-отправлен успешно.')
            # Запрос POST в удобном для чтения формате .json
            log(3, f"{json.dumps(response, indent = 4, ensure_ascii=False)}")
        
        # В случае неудачного запроса (при ошибке).
        except: 
            log(2, f'Запрос POST-не отправлен!')

if __name__ == "__main__":
    request_post('message')
    