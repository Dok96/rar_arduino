import time
import threading
import snap7
from config import plc_ip, rack, slot, retry_delay, en_print, en_gen_report ,en_summ_message
from plc_read.readTrigger import read_trigger_def  # читаем триггер о формировании отчёта
from plc_read.plcReadTime import read_time_plc  # читаем время для отчёта
from plc_read.plcResetTrigger import res_trigger  # сбрасываем триггер о формировании отчёта
from report.copyTemplateReport import copy_file_with_replace
from plc_read.readMessage import read_summ_message
from report.reportHead import rep_head
from report.saveReportPdfXlsx_2 import save_report_to_files, get_pdf_path
from report.reportAlarm import report_alarm
from print.print_def_2 import print_file
from plc_connection.plc_conect import connect_to_plc
from plc_connection.ping import ping_plc
import logging

# Глобальная переменная для завершения программы
exit_flag = False
plc = None

# Настройка логирования
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S" )
logger = logging.getLogger(__name__)

# Функция для обработки ввода пользователя
def user_input_handler():
    global exit_flag  # Объявляем глобальную переменную перед её использованием
    while not exit_flag:
        user_input_exit = input("Ожидание триггера. Завершить программу? (y/n): ").strip().lower()
        if user_input_exit == "y" or "у":
            print("Программа завершена пользователем.")
            exit_flag = True
            break

if __name__ == "__main__":
    # Создаём объект PLC
    plc = snap7.client.Client()

    try:
        # Запускаем поток для обработки ввода пользователя
        input_thread = threading.Thread(target=user_input_handler, daemon=True)
        input_thread.start()

        # Основной цикл работы программы
        while not exit_flag:
            try:
                # Проверяем доступность PLC с помощью ping
                if not ping_plc(plc_ip):
                    print(f"PLC недоступен по адресу {plc_ip}. Повторная попытка через {retry_delay} секунд...")
                    logger.error(f"PLC недоступен по адресу {plc_ip}. Повторная попытка через {retry_delay} секунд...")
                    if plc and plc.get_connected():
                        plc.disconnect()
                        print("Соединение с PLC закрыто из-за отсутствия ping.")
                        logger.error("Соединение с PLC закрыто из-за отсутствия ping.")
                    time.sleep(retry_delay)
                    continue

                # Подключаемся к PLC, если соединение не установлено
                if not plc.get_connected():
                    print("Соединение с PLC потеряно. Пытаемся переподключиться... ")
                    logger.error("Соединение с PLC потеряно. Пытаемся переподключиться...")
                    connect_to_plc(plc, plc_ip, rack, slot)
                    continue

                # Читаем триггер
                trigger_report = read_trigger_def(plc)

                # Проверяем, изменилось ли значение триггера
                if trigger_report:
                    print("Триггер активен. Читаем время...")
                    logger.info("Триггер активен. Читаем время...")


                    # читаем количество сообщений
                    summ_message = read_summ_message(plc)
                    print(f'Количество сообщений: {summ_message}')
                    logger.info(f'Количество сообщений: {summ_message}')

                    # Вызываем функцию чтения времени и получаем значения
                    time_start, time_stop, len_product = read_time_plc(plc)  # Передаём объект PLC

                    # Проверяем, что значения не равны None
                    if time_start and time_stop:
                        print(f"Время начала: {time_start}")
                        print(f"Время окончания: {time_stop}")
                        logger.info(f"Время начала: {time_start}, Время окончания: {time_stop}")

                    copy_file_with_replace()  # копируем заготовку для отчёта
                    print(f'xlsx шаблон подготовлен')
                    logger.info(f'xlsx шаблон подготовлен')

                    r_product_len = len_product

                    if en_gen_report == 1:
                    ############ Формирование отчёта##################
                        if summ_message > 0:
                            # если есть сообщения о дефектах
                            rep_head( time_start, time_stop, r_product_len)      # шапка
                            report_alarm(plc, summ_message)  # запись alarm
                            dir_pdf_file = save_report_to_files()  # сохранение файла в plf, xl
                            pdf_direct = get_pdf_path()  # Получаем путь через функцию
                            print(f'Путь PDF файла: {pdf_direct}')
                            logger.info(f'Путь PDF файла: {pdf_direct}')

                        else:
                            # если провод без дефекта
                            rep_head( time_start, time_stop, r_product_len)      # шапка
                            dir_pdf_file = save_report_to_files()  # сохранение файла в plf, xl
                            pdf_direct = get_pdf_path()  # Получаем путь через функцию для печати файла
                            print(f'Путь PDF файла: {pdf_direct}')
                            logger.info(f'Путь PDF файла: {pdf_direct}')

                        print(f"print direction : {pdf_direct}")
                        logger.info(f"print direction : {pdf_direct}")

                    rep_dir = pdf_direct

                    if (en_print == 1 and en_gen_report == 1 and
                            (( summ_message > 0 and en_summ_message ==1) or en_summ_message ==0 )) : #разрешение на вывод печати
                        print_file(rep_dir)

                    # Сбрасываем триггер
                    res_trigger(plc)
                    print("Триггер сброшен \n Завершить программу? (y/n): ")

            except Exception as e:
                if "Connection reset by peer" in str(e):
                    print("Ошибка: Соединение с PLC разорвано (Connection reset by peer).")
                    logger.info("Ошибка: Соединение с PLC разорвано (Connection reset by peer).")
                    if plc and plc.get_connected():
                        plc.disconnect()
                        print("Соединение с PLC закрыто.")
                        logger.info("Соединение с PLC закрыто.")
                    print("Ожидание восстановления связи с PLC...")
                    logger.info("Ожидание восстановления связи с PLC...")
                else:
                    print(f"Ошибка при работе с ПЛК: {e}")
                    logger.error(f"Ошибка при работе с ПЛК: {e}",exc_info=True )

                # Проверяем доступность PLC через ping
                while not ping_plc(plc_ip):
                    print(f"PLC недоступен по адресу {plc_ip}. Повторная попытка через {retry_delay} секунд...")
                    logger.info(f"PLC недоступен по адресу {plc_ip}. Повторная попытка через {retry_delay} секунд...")
                    time.sleep(retry_delay)

                # Пытаемся восстановить соединение
                print("PLC доступен. Пытаемся восстановить соединение...")
                logger.info("PLC доступен. Пытаемся восстановить соединение...")
                connect_to_plc(plc, plc_ip, rack, slot)

            time.sleep(1)

    finally:
        exit_flag = True

        # Закрываем соединение с ПЛК при выходе
        if plc and plc.get_connected():
            plc.disconnect()
            print("Соединение с ПЛК закрыто.")