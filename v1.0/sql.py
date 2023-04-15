# -*- coding: utf-8 -*-
# --- Встроенные модули.
import sqlite3
# --- Скаченные модули.
# --- самописные модули.
from log import log


db_name = 'sqlite_python.db'


def sql_connection()-> object:
    """
    Соединение с БД.
    """
    
    try:
        # Подключение к существующей базе данных
        connection = sqlite_connection = sqlite3.connect(db_name)

        # log(3, f"Соединение с БД ({db_name}) - успешно.")
        return connection        

    except sqlite3.Error as error:
        log(1, f"Ошибка соединения с БД. Текст ошибки:\n{error}")
        
def sql_connection_close(connection: object):
    """
    Закрытие соединение с БД.
    """

    try:
        connection.close()
        # log(3, f"Соединение с БД закрыто.")

    except sqlite3.Error as error:
        log(1, f"Ошибка  БД. Текст ошибки:\n{error}")

def sql_select(querry: str) -> object:
    """
    Обработчик запросов к БД типа: SELECT.
    При ошибке возвращает: False.
    """

    connection = sql_connection()
    cursor = connection.cursor()

    # Впоследствии `.commit()` вызывается автоматически.
    with connection:
        try:
            cursor.execute(querry) 
            # log(3, f"Запрос выполнен - успешно.") 
            response = cursor.fetchall()     
              
        except sqlite3.Error as error:
            log(1, f"Ошибка. Текст ошибки:\n{error}")
            response = False

    sql_connection_close(connection)
    return response

def sql_insert(querry: str) -> bool:
    """
    Обработчик запросов к БД типа: INSERT.
    При ошибке возвращает: False.
    """ 

    connection = sql_connection()
    cursor = connection.cursor()

    # Впоследствии `.commit()` вызывается автоматически.
    with connection:
        try:
            cursor.execute(querry) 
            # log(3, f"Запрос выполнен - успешно.")
            response = True     
              
        except sqlite3.Error as error:
            log(1, f"Ошибка. Текст ошибки:\n{error}")
            
            if 'UNIQUE' in str(error):
                log(2, f"В Бд уже есть такая вакансия!")
                response = False
            

    sql_connection_close(connection)
    return response

if __name__ == "__main__":
    print(sql_select("select sqlite_version();"))
    