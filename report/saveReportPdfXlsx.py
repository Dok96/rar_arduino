
from openpyxl import load_workbook
from config import curr_report, dist_report_xlsx, dist_report_pdf
import os
from datetime import datetime
import win32com.client
import pythoncom  # Для работы с COM-объектами

# Глобальная переменная для хранения пути к PDF-файлу
global_output_file_pdf = None

def save_report_to_files():
    global global_output_file_pdf
    template_path = curr_report
    base_output_path_xlsx = dist_report_xlsx
    base_output_path_pdf = dist_report_pdf

    try:
        now = datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%m')
        day = now.strftime('%d')
        timestamp = now.strftime('%H-%M-%S')

        # Формируем пути к директориям
        output_dir_xlsx = os.path.join(base_output_path_xlsx, year, month, day)
        output_dir_pdf = os.path.join(base_output_path_pdf, year, month, day)
        os.makedirs(output_dir_xlsx, exist_ok=True)
        os.makedirs(output_dir_pdf, exist_ok=True)

        # Формируем пути к файлам
        output_file_xlsx = os.path.join(output_dir_xlsx, f"{timestamp}.xlsx").replace("\\", "/")
        output_file_pdf = os.path.join(output_dir_pdf, f"{timestamp}.pdf").replace("\\", "/")
        global_output_file_pdf = output_file_pdf


        # Открываем шаблон Excel
        wb = load_workbook(template_path)
        ws = wb.active
        wb.save(output_file_xlsx)
        print(f"Данные успешно записаны в файл: {output_file_xlsx}")

        # Преобразуем Excel в PDF с помощью COM-интерфейса
        excel = None
        workbook = None
        try:
            pythoncom.CoInitialize()
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Visible = False

            if os.path.exists(output_file_xlsx):
                workbook = excel.Workbooks.Open(output_file_xlsx)
                workbook.ExportAsFixedFormat(0, output_file_pdf)
                workbook.Close(SaveChanges=False)
                print(f"Данные успешно записаны в файл: {output_file_pdf}")
            else:
                print("Ошибка: Excel-файл не найден.")
        except Exception as e:
            print("Ошибка при преобразовании в PDF:", e)
        finally:
            if 'workbook' in locals() and workbook:
                workbook.Close(SaveChanges=False)
            if 'excel' in locals() and excel:
                excel.Quit()
            pythoncom.CoUninitialize()

    except Exception as e:
        print("Ошибка при сохранении отчета:", e)


# Функция для получения значения global_output_file_pdf
def get_pdf_path():
    return global_output_file_pdf