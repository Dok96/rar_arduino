import os
import time
import win32api
import win32print

def print_file(rep_dir, max_retries=5, delay=1):
    """
    Отправляет PDF-файл на печать через принтер по умолчанию.
    При ошибке делает повторные попытки (до max_retries раз).

    :param rep_dir: Путь к PDF-файлу
    :param max_retries: Максимальное количество попыток
    :param delay: Задержка между попытками (в секундах)
    """
    if not os.path.exists(rep_dir):
        print(f"Ошибка: файл не найден по пути {rep_dir}")
        return False

    for attempt in range(1, max_retries + 1):
        try:
            # Получаем имя принтера по умолчанию
            default_printer = win32print.GetDefaultPrinter()
            print(f"[Попытка {attempt}] Используется принтер: {default_printer}")

            # Пробуем отправить на печать
            win32api.ShellExecute(0, "print", rep_dir, None, ".", 0)
            print(f"Файл успешно отправлен на печать: {rep_dir}")
            return True

        except Exception as e:
            print(f"[Ошибка] Попытка {attempt} завершена с ошибкой: {e}")

            if attempt < max_retries:
                print(f"Повторная попытка через {delay} секунд...")
                time.sleep(delay)
            else:
                print("Не удалось отправить файл на печать после всех попыток.")
                return False