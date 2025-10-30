
from openpyxl import load_workbook
from config import destination_report, destinationXl, destinationPDF
import os
from datetime import datetime
import win32com.client
import pythoncom
import win32security
import ntsecuritycon as con


# Глобальная переменная для хранения пути к PDF-файлу
global_output_file_pdf = None


# def grant_full_control_to_everyone(file_path):
#     """Функция даёт полный доступ всем пользователям"""
#     try:
#         user, domain, type = win32security.LookupAccountName("", "Everyone")
#         sd = win32security.GetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION)
#         dacl = sd.GetSecurityDescriptorDacl()
#
#         # Добавляем разрешение: Everyone - Full Control
#         dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_ALL_ACCESS, user)
#
#         sd.SetSecurityDescriptorDacl(1, dacl, 0)
#         win32security.SetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION, sd)
#         print(f"Доступ открыт для 'Все': {file_path}")
#     except Exception as e:
#         print(f"Ошибка при установке прав на файл {file_path}: {e}")

def grant_read_access_to_everyone(file_path):
    try:
        sid = win32security.ConvertStringSidToSid("S-1-1-0")  # Everyone
        sd = win32security.GetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION)
        dacl = sd.GetSecurityDescriptorDacl()

        if dacl is None:
            dacl = win32security.ACL()

        dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_GENERIC_READ, sid)

        sd.SetSecurityDescriptorDacl(1, dacl, 0)
        win32security.SetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION, sd)

        print(f"[OK] Доступ для 'Все' установлен: {file_path}")
    except Exception as e:
        print(f"[ERROR] Не удалось установить права для 'Все': {e}")


def save_report_to_files(record):
    global global_output_file_pdf
    template_path = destination_report
    base_output_path_xlsx = destinationXl
    base_output_path_pdf = destinationPDF

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
        output_file_xlsx = os.path.join(output_dir_xlsx, f"{timestamp}_id_{record['ID']}.xlsx").replace("\\", "/")
        output_file_pdf = os.path.join(output_dir_pdf, f"{timestamp}_id_{record['ID']}.pdf").replace("\\", "/")
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
                print(f"PDF успешно сохранён: {output_file_pdf}")

                # После создания PDF — устанавливаем права
                if os.path.exists(output_file_pdf):
                    grant_read_access_to_everyone(output_file_pdf)
                else:
                    print("Ошибка: PDF-файл не найден после сохранения.")

            else:
                print("Ошибка: Excel-файл не найден.")
        except Exception as e:
            print("Ошибка при преобразовании в PDF:", e)
        finally:
            # Явное закрытие Excel
            if 'workbook' in locals() and locals()['workbook']:
                try:
                    locals()['workbook'].Close(SaveChanges=False)
                except:
                    pass
            if 'excel' in locals() and locals()['excel']:
                try:
                    locals()['excel'].Quit()
                except:
                    pass
            pythoncom.CoUninitialize()

    except Exception as e:
        print("Ошибка при сохранении отчета:", e)


# Функция для получения значения global_output_file_pdf
def get_pdf_path():
    return global_output_file_pdf