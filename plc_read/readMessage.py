from config import db_number, n_summ_message, n_message_size

def read_summ_message(plc):
    try:
        #summ_message= None
        # Чтение данных из ПЛК
        summ_message_bytes = plc.db_read(db_number, n_summ_message, n_message_size)

        # Преобразование массива байтов в целое число
        summ_message = int.from_bytes(summ_message_bytes, byteorder='big')  # 'big' или 'little' зависит от порядка байтов в ПЛК

        return summ_message

    except Exception as e:
        print(f"Ошибка: {e}")
        return None