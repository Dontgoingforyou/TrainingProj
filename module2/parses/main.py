from module2.database import SessionLocal, create_db
from module2.parses.saver import download_spimex_report
from module2.parses.utils import parse_spimex_xlsx


def main():
    """Основной процесс: скачивание, парсинг, сохранение."""
    create_db()
    file_path = download_spimex_report()

    if file_path:
        session = SessionLocal()

        try:
            parse_spimex_xlsx(file_path, session)
        finally:
            session.close()
    else:
        print("Не удалось скачать отчет.")


if __name__ == "__main__":
    main()