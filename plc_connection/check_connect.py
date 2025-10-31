# plc_connection/check_and_connect.py
import time
import logging
import snap7
from config import plc_ip, rack, slot, retry_delay
from plc_connection.plc_conect import connect_to_plc
from plc_connection.ping import ping_plc

logger = logging.getLogger(__name__)

def ensure_plc_connection(plc: snap7.client.Client) -> bool:
    """
    Проверяет доступность PLC через ping и подключается к нему при необходимости.
    Возвращает True, если соединение установлено и стабильно.
    Возвращает False, если PLC недоступен или подключение не удалось.
    """

    # 1. Проверяем доступность через ping
    if not ping_plc(plc_ip):
        logger.error(f"PLC недоступен по адресу {plc_ip}. Повторная попытка через {retry_delay} секунд...")
        if plc and plc.get_connected():
            plc.disconnect()
            logger.error("Соединение с PLC закрыто из-за отсутствия ping.")
        time.sleep(retry_delay)
        return False

    # 2. Если нет соединения — подключаемся
    if not plc.get_connected():
        logger.error("Соединение с PLC потеряно. Пытаемся переподключиться...")
        try:
            connect_to_plc(plc, plc_ip, rack, slot)
        except Exception as e:
            logger.error(f"Не удалось подключиться к PLC: {e}")
            time.sleep(retry_delay)
            return False

    return True