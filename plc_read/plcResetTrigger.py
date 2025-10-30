from config import db_number
from config import trig_address
def res_trigger(plc):
    try:

        byte_data = plc.db_read(db_number, trig_address, 1)
        current_byte = byte_data[0]

        # Сбрасываем бит 0 в 0
        new_byte = current_byte & ~(1 << 0)

        # Записываем измененный байт обратно в блок данных
        plc.db_write(db_number, trig_address, bytearray([new_byte]))


    except Exception as e:
        print(f'ошибка : {e}')






