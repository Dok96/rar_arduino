import os
from email.policy import default

import win32api
import win32print

def print_file(rep_dir):
    """
    Отправляет файл на печать с использованием системного принтера по умолчанию.

    :param rep_dir: Путь к файлу, который нужно напечатать.
    """
    if  not os.path.exists(rep_dir): # если нет файла тогда:
        print(f"ошибка: файл не найден по пути {rep_dir}")
        return

    try:
        # получаем имя принтера по умолчанию
        default_printer= win32print.GetDefaultPrinter()
        print(f"Используется принтер по умолчанию: {default_printer}")

        #отправляем на печать
        win32api.ShellExecute(0, "print",rep_dir,None, ".",0)
        print(f"Файл успешно отправлен на печать: {rep_dir}")

    except Exception as e:
        print(f"ошибка при отправке {e}")





