import os

def load_config(file_path):
    """
    Загружает конфигурацию из текстового файла.
    Возвращает словарь с параметрами.
    """
    config = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Пропускаем комментарии и пустые строки
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Разделяем строку на ключ и значение
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Преобразуем числовые значения
                    if value.isdigit():
                        value = int(value)
                    elif value.replace('.', '', 1).isdigit():
                        value = float(value)

                        # Если значение является путем, заменяем обратные слеши на прямые
                    if key in ["dist_report_pdf", "dist_report_xlsx","template_report",
                        "blank_report","template_Lump_report", "lump_report",
                                "", "", "", ""]:
                        value = value.replace("\\", "/")

                    config[key] = value
    except FileNotFoundError:
        print(f"Файл конфигурации не найден: {file_path}")
    except Exception as e:
        print(f"Ошибка при чтении конфигурации: {e}")

    return config

# Путь к файлу конфигурации
CONFIG_FILE = "config.txt"

# Загрузка конфигурации
config = load_config(CONFIG_FILE)

running = True # общая переменная


# # Доступ к параметрам через глобальные переменные
# source = config.get("source")
# destination = config.get("destination")
# interval = config.get("interval", 1)  # Значение по умолчанию
# m_retries = config.get("m_retries", 200)
#
# source_template_Xl = config.get("source_template_Xl")


#==Report==
source_template_report = config.get("template_report")

dist_report_pdf= config.get("dist_report_pdf") # путь для pdf
dist_report_xlsx = config.get("dist_report_xlsx") # путь для xlsx
curr_report = config.get("curr_report") # путь для  шаблона xlsx
blank_report = config.get("blank_report") # путь загатовки  для  шаблона xlsx

dist_template_Lump_report = config.get("dist_template_Lump_report") #шаблон Lump (для подмены)
dist_lump_report = config.get("dist_lump_report") #отчёт (текущий отчёт по дефектам Lump)

#==PLC==
#==connect
plc_ip = config.get("plc_ip")
rack = config.get("rack")
slot = config.get("slot")
retry_delay = config.get("retry_delay", 5)
MAX_retry_delay= config.get("MAX_retry_delay", 5)

#==message (длина и тригер формирования сообщения)
#  номер дата блока
db_number = config.get("db_number")
# размещение тега триггера
offset_len = config.get("offset_len")

# размещение тега триггера
trig_address = config.get("trig_address")
trig_size = config.get("trig_size")

# время опроса тегов
time_tag = config.get("time_tag", 0.2)

# длина производственная
len_prod_offset = config.get("len_prod_offset")
len_prod_size =4

n_summ_message = config.get("n_summ_message")
n_message_size = config.get("n_message_size")


# включить печать
en_print = config.get("en_print")

start_h = config.get("start_h")
start_m = config.get("start_m")
start_s = config.get("start_s")
stop_h = config.get("stop_h")
stop_m = config.get("stop_m")
stop_s = config.get("stop_s")
time_dSize = config.get("time_dSize")

#print(f"{db_number} ; {offset_len}, {offset_trigger}")

en_copy_mdb = config.get("en_copy_mdb")
en_read_mdb =  config.get("en_read_mdb")
en_gen_report = config.get("en_gen_report")

# =1 для включение печати если сумма сообщение alarm больше 0, если 0 тогда печать даже пустых протоколов
en_summ_message = config.get("en_summ_message")



