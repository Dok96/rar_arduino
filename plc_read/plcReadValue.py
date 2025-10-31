import snap7
from config import  db_number, start_h, start_m, start_s, stop_h, stop_m, stop_s, time_dSize, len_prod_offset, len_prod_size

def read_plc(plc):
    try:

        # Чтение времени начала
        hours_data = plc.db_read(db_number, start_h, time_dSize)
        s_hours = int.from_bytes(hours_data, byteorder='big')

        minute_data = plc.db_read(db_number, start_m, time_dSize)
        s_minutes = int.from_bytes(minute_data, byteorder='big')

        second_data = plc.db_read(db_number, start_s, time_dSize)
        s_seconds = int.from_bytes(second_data, byteorder='big')

        time_start = f"{s_hours:02}:{s_minutes:02}:{s_seconds:02}"

        # Чтение времени окончания
        hours_data = plc.db_read(db_number, stop_h, time_dSize)
        stp_hours = int.from_bytes(hours_data, byteorder='big')

        minute_data = plc.db_read(db_number, stop_m, time_dSize)
        stp_minutes = int.from_bytes(minute_data, byteorder='big')

        second_data = plc.db_read(db_number, stop_s, time_dSize)
        stp_seconds = int.from_bytes(second_data, byteorder='big')

        time_stop = f"{stp_hours:02}:{stp_minutes:02}:{stp_seconds:02}"

        #читаем производственную длину
        len_buffer=plc.db_read(db_number, len_prod_offset, len_prod_size)
        len_product =  snap7.util.get_real(len_buffer, 0) # Преобразуем 4 байта в float


        return time_start, time_stop, len_product  # Возвращаем значения

    except Exception as e:
        print(f"Ошибка: {e}")
        return None, None, None  # Возвращаем None, если произошла ошибка