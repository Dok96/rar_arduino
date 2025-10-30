import os
import shutil
from config import blank_report,curr_report

# копирование шоблона
def copy_file_with_replace():
    source_path = curr_report
    destination_path=blank_report


    """
    Копирует файл из source_path в destination_path.
    Если файл уже существует в destination_path, он будет заменён.
    :param source_path: Путь к исходному файлу.
    :param destination_path: Путь к целевому файлу.
    """
    try:
        # Проверяем, существует ли исходный файл
        if not os.path.exists(source_path):
            print(f"Ошибка: Исходный файл не найден: {source_path}")
            return

        # Проверяем, существует ли целевой файл
        if os.path.exists(destination_path):
            print(f"Файл уже существует в целевой директории: {destination_path}")
            print("Заменяем файл...")

        # Копируем файл (shutil.copy2 сохраняет метаданные файла)
        shutil.copy2(source_path, destination_path)
        print(f"Файл успешно скопирован: {destination_path}")

    except Exception as e:
        print(f"Ошибка при копировании файла: {e}")


# if __name__ == "__main__":
#     # Вызываем функцию для копирования
#     copy_file_with_replace()