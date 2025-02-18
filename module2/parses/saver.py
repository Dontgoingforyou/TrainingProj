import os
import requests
from datetime import datetime, timedelta

# Папка для сохранения файлов
SAVE_DIR = "spimex_reports"
os.makedirs(SAVE_DIR, exist_ok=True)

BASE_URL = "https://spimex.com/upload/reports/oil_xls/oil_xls_"


def find_latest_spimex_report():
    """Ищет последний доступный файл, начиная с текущей даты и двигаясь назад."""
    today = datetime.today()

    for i in range(30):
        date_str = (today - timedelta(days=i)).strftime("%Y%m%d")
        report_url = f"{BASE_URL}{date_str}162000.xls"

        response = requests.head(report_url, timeout=10)

        if response.status_code == 200:
            print(f"Найден доступный файл: {report_url}")
            return report_url

    print("Не удалось найти файл за последние 30 дней.")
    return None


def download_spimex_report():
    """Скачивает последний найденный отчет."""
    report_url = find_latest_spimex_report()
    if not report_url:
        return None

    filename = os.path.basename(report_url)
    file_path = os.path.join(SAVE_DIR, filename)

    response = requests.get(report_url, stream=True, timeout=10)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Файл сохранен: {file_path}")
        return file_path
    else:
        print(f"Ошибка скачивания: {response.status_code}")
        return None
