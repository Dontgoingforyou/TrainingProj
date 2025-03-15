import pandas as pd
from datetime import datetime
from module4.async_parses.model import SpimexTradingResult
from sqlalchemy.ext.asyncio import AsyncSession


async def parse_spimex_xlsx(file_path, session: AsyncSession):
    """Парсит XLSX файл и сохраняет в БД."""

    engine = "openpyxl" if file_path.endswith(".xlsx") else "xlrd"
    df = pd.read_excel(file_path, engine=engine, header=None)

    # Поиск строки "Единица измерения: Метрическая тонна"
    target_row_index = None
    for index, row in df.iterrows():
        if row.astype(str).str.contains("Единица измерения: Метрическая тонна", na=False).any():
            target_row_index = index
            break

    if target_row_index is None:
        raise ValueError("Таблица 'Единица измерения: Метрическая тонна' не найдена в файле.")

    print(f"Найдено 'Единица измерения: Метрическая тонна' на строке: {target_row_index}")

    # Загрузка данных начиная со строки заголовков (следующей строки)
    df = pd.read_excel(file_path, engine=engine, skiprows=target_row_index + 1)

    # Очистка названий столбцов
    df.columns = df.columns.astype(str).str.replace("\n", " ").str.strip()

    print(f"Столбцы после очистки: {df.columns.tolist()}")

    # Проверка существования ключевых столбцов
    required_columns = {
        "Код Инструмента": "exchange_product_id",
        "Наименование Инструмента": "exchange_product_name",
        "Базис поставки": "delivery_basis_name",
        "Объем Договоров в единицах измерения": "volume",
        "Обьем Договоров, руб.": "total",
        "Количество Договоров, шт.": "count"
    }

    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"Столбец '{col}' не найден в файле. Доступные столбцы: {df.columns.tolist()}")

    def to_numeric_column(col):
        """ Преобразует в числовой формат. """
        return pd.to_numeric(col, errors="coerce").fillna(0)

    # Преобразование всех числовых данных в float, если возможно
    df = df[df["Код Инструмента"] != "Итого:"]

    df["Объем Договоров в единицах измерения"] = to_numeric_column(df["Объем Договоров в единицах измерения"])
    df["Обьем Договоров, руб."] = to_numeric_column(df["Обьем Договоров, руб."])
    df["Количество Договоров, шт."] = to_numeric_column(df["Количество Договоров, шт."])
    df["Изменение рыночной цены к цене предыдуего дня"] = to_numeric_column(
        df["Изменение рыночной цены к цене предыдуего дня"])

    # Преобразование цены
    df["Цена (за единицу измерения), руб."] = to_numeric_column(df["Цена (за единицу измерения), руб."])
    df["Цена в Заявках (за единицу измерения)"] = to_numeric_column(df["Цена в Заявках (за единицу измерения)"])

    # Преобразование столбца "Наименование Инструмента" в строковый тип
    df["Наименование Инструмента"] = df["Наименование Инструмента"].astype(str)

    print(f"Типы данных столбцов:\n{df.dtypes}")

    # Фильтрация строк, где числовые столбцы имеют значения больше нуля
    df = df[df["Объем Договоров в единицах измерения"] > 0]
    df = df[df["Обьем Договоров, руб."] > 0]
    df = df[df["Количество Договоров, шт."] > 0]

    print(f"Количество строк после фильтрации: {df.shape[0]}")

    # Добавляем полей
    df["oil_id"] = df["Код Инструмента"].astype(str).str[:4]
    df["delivery_basis_id"] = df["Код Инструмента"].astype(str).str[4:7]
    df["delivery_type_id"] = df["Код Инструмента"].astype(str).str[-1]
    df["date"] = datetime.now()

    # Сохранение в БД
    try:
        for _, row in df.iterrows():
            try:
                trading_result = SpimexTradingResult(
                    exchange_product_id=row["Код Инструмента"],
                    exchange_product_name=row["Наименование Инструмента"],
                    oil_id=row["oil_id"],
                    delivery_basis_id=row["delivery_basis_id"],
                    delivery_basis_name=row["Базис поставки"],
                    delivery_type_id=row["delivery_type_id"],
                    volume=float(row["Объем Договоров в единицах измерения"]),  # явное приведение к float
                    total=float(row["Обьем Договоров, руб."]),  # явное приведение к float
                    count=int(row["Количество Договоров, шт."]),  # явное приведение к int
                    date=row["date"],
                )
                session.add(trading_result)
            except Exception as e:
                print(f"Ошибка при обработке строки {row['Код Инструмента']}: {e}")
                continue

        await session.commit()
        print(f"Данные из {file_path} успешно сохранены в БД.")
    except Exception as e:
        print(f"Ошибка при сохранении данных в БД: {e}")
        await session.rollback()
