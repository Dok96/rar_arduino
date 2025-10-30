from cx_Freeze import setup, Executable

# Настройки для сборки
build_options = {
    "packages": [],  # Добавьте здесь пакеты, которые нужно включить
    "include_files": [
        "config.py",  # Включаем файл конфигурации
        "dt/",
        "mdb/",               # Включаем папку для работы с базой данных
        "plc_connection/",  # Включаем папку с модулями для подключения к PLC
        "plc_read/",         # Включаем папку с модулями для чтения данных
        "print/" ,
        "report/"           # Включаем папку для работы с отчетами

    ],
    "excludes": []  # Исключаем ненужные модули
}


setup(
    name="YourAppName",
    version="1.0",
    description="Your application description",
    executables=[Executable("main_exe2.py", icon="path/to/icon.ico")],
)

#   python setup.py build  "вставить в консоль для конвертировании в exe"
