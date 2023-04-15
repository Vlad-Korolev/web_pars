import sqlite3
from log import log


db_name = 'sqlite_python.db'


# try:
#     sqlite_connection = sqlite3.connect('sqlite_python.db')
#     cursor = sqlite_connection.cursor()
#     print("База данных создана и успешно подключена к SQLite")

#     sqlite_select_query = "select sqlite_version();"
#     cursor.execute(sqlite_select_query)
#     record = cursor.fetchall()
#     print("Версия базы данных SQLite: ", record)
#     cursor.close()

# except sqlite3.Error as error:
#     print("Ошибка при подключении к sqlite", error)
# finally:
#     if (sqlite_connection):
#         sqlite_connection.close()
#         print("Соединение с SQLite закрыто")


def sql_connection()-> object:
    """
    Соединение с БД.
    """
    
    try:
        # Подключение к существующей базе данных
        connection = sqlite_connection = sqlite3.connect(db_name)

        log(3, f"Соединение с БД ({db_name}) - успешно.")
        return connection        

    except sqlite3.Error as error:
        log(1, f"Ошибка соединения с БД. Текст ошибки:\n{error}")
        
def sql_connection_close(connection: object):
    """
    Закрытие соединение с БД.
    """

    try:
        connection.close()
        log(3, f"Соединение с БД закрыто.")

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
            log(3, f"Запрос выполнен - успешно.") 
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
            log(3, f"Запрос выполнен - успешно.")
            response = True     
              
        except sqlite3.Error as error:
            log(1, f"Ошибка. Текст ошибки:\n{error}")
            response = False

    sql_connection_close(connection)
    return response

if __name__ == "__main__":
    # print(sql_select("select sqlite_version();"))
    pass
    