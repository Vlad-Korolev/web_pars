# --- Встроенные модули.
import datetime, os, zipfile, inspect
# --- Скаченные модули.
# --- самописные модули.


# Типы событий.
events = {1: "   ERROR   ", 
          2: "  WARNING  ", 
          3: "INFORMATION"}
# Режим отладки (вывод всех сообщений помимо файла еще и в консоль).
debug = 0
# Максимальный размер лога в мегабайтах (до архивации).
max_log_size = 100
# Имя директории в корне для хранения лог-файлов.
log_folder = "log"

# Служебные переменные:
log_name = "1.log"


 
def archive_log(log_file: str):
    """
    Архивация log-файла, при его заполнении.
    """ 

    try:
        archive = zipfile.ZipFile(f'{log_folder}/{log_file}.zip', 'w', zipfile.ZIP_DEFLATED)
        archive.write(f'{log_folder}/{log_file}')
        archive.close()
        os.remove(f'{log_folder}/{log_file}')
        
    except:
        log(1, f"Ошибка. Архивации заполненного log-фала: {log_file} не удалась.") 

def check_log_folder():
    # Директория для хранения log-файлов не найдена.
    if not os.path.exists(log_folder):
        print(f"[log] Ошибка. Не удалось найти папку для хранения log-файлов: {log_folder}")
        
        try:        
            os.mkdir(log_folder)
            log(2, f"Папка для хранения log-файлов не найдена, создана: {log_folder}")

        except:
            print(f"[log] Ошибка. Не удалось создать папку для хранения log-файлов: {log_folder}")
            quit()

def check_log_files():
    global log_name

    log_files = os.listdir(f"{log_folder}")

    if log_files:
        size_last_log = os.path.getsize(f"{log_folder}/{max(log_files)}")

        if size_last_log >= (max_log_size * 1000000):
            log_name = str(int(max(log_files).split(".")[0]) + 1) + ".log"
            if not ".zip" in max(log_files): 
                archive_log(max(log_files))               
  
        else:
            log_name = max(log_files) 

def log(event_number: int = 1, message: str = "Log вызван без аргументов.", console = False):
    """
    Запись события в log-файл (вывод на консоль, при вклчюенном console = True).
    """

    check_log_folder()
    check_log_files()

    # Блок проверки переданных значений в ф-цию log.
    # event_number неправильный, нету в events.
    if not event_number in events: events[event_number] = f"Отсутствует событие с ключом: {event_number}"
    # message с неверным типом данных.
    if not type(message) is str: message = "При вызове в ф-цию Log отправлен не верный тип. Нужен тип: str"

    
    # Получение текущей даты и времени.
    now = datetime.datetime.now()
    current_date = now.strftime("%d.%m.%Y %H:%M:%S") # ms: %S.%f

    # Запись сообщения в log-файл.
    try:
        with open(f"{log_folder}/{log_name}", "a+", encoding="utf-8") as file:

            source_file_name = inspect.stack()[1][1].split('\\')[-1]
            source_function  = inspect.stack()[1][3]

            log_message = f"[{current_date}] [{events[event_number]}] [{source_file_name}]-[{source_function}] {message}"
            file.write(log_message + "\n")
            
            # Режим отладки включен.
            if debug == 1:
                print(log_message)
            else:
                # Console = true.
                if console:
                    print(message) 

    except:
        print(f"[log] Ошибка при записи сообщения в log-файл: {log_folder}/{log_name}.")

if __name__ == "__main__":
    print("Начало выполнения")
    log(1, "text_message_1", console = True)
    log(2, "text_message_2")
    log(3, "text_message_3")
    log(1, "text_message_4")
    log(2, "text_message_5", console = True)
    log(3, "text_message_6")
    log(1, "text_message_7")
    log(2, "text_message_8")
    log(3, "text_message_9")
    log("asdasd123", 123, console = True)
    log()




