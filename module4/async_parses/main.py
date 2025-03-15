import time
import asyncio

from module4.database import AsyncSessionLocal, create_db
from module4.async_parses.saver import download_spimex_report, find_latest_spimex_report
from module4.async_parses.utils import parse_spimex_xlsx


async def main():
    """Основной процесс: скачивание, парсинг, сохранение."""

    start_time = time.time()

    await create_db()
    files_to_download = await find_latest_spimex_report(n=5)

    if files_to_download:
        tasks = [download_spimex_report(url) for url in files_to_download]
        downloaded_files = await asyncio.gather(*tasks)

        async with AsyncSessionLocal() as session:
            for file in filter(None, downloaded_files):  # Пропуск None, если файлы не скачались
                await parse_spimex_xlsx(file, session)
    else:
        print("Не удалось скачать отчет.")

    end_time = time.time()
    print(f"\nВремя выполнения (асинхронно): {end_time - start_time:.2f} секунд\n")


if __name__ == "__main__":
    asyncio.run(main())