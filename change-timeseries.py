import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from typing import List

def load_dataframe_from_file(path: str) -> pd.DataFrame:
    """
    Загрузка таблицы из CSV файла.

    Args:
        path (str): Путь до CSV файла.

    Returns:
        pd.DataFrame: Таблица с одним столбцом "timestamp".

    Raises:
        FileNotFoundError: Если файл не существует.
        ValueError: Если в файле неверная структура или данные не читаются.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл не найден: {path}")

    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise ValueError(f"Ошибка чтения CSV: {e}")

    if df.shape[1] != 1:
        raise ValueError("Ожидался ровно один столбец во входном CSV.")

    df.columns = ["timestamp"]

    return df


def create_periodic_dataframe(
        start_timedate_point: str, periods: int, freq: str
) -> pd.DataFrame:
    """
    Создание таблицы с временными метками
    в строковом представлении,
    синтетическим способом - через распределительную функцию.

    Args:
        start_timedate_point (str): Строка "YYYY-MM-DD HH:MM:SS"
        periods (int): Число создаваемых значений (число меток в столбце)
        freq (str): Шаг между значениями

    Returns:
        pd.DataFrame: Заполненная таблица при успехе, и пустая таблица при ошибке.

    Raises:
        Exception: Любые исключения, возникающие в процессе создания таблицы
    """
    try:
        timestamps = pd.date_range(
            start=start_timedate_point,
            periods=periods,
            freq=freq
        )

        return pd.DataFrame({"timestamp": timestamps})

    except Exception as e:
        print(f"Ошибка при создании строковых временных меток: {e}")


def convert_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """
    Преобразование строковых меток во временной формат datetime.

    Args:
        df (pd.DataFrame): Таблица, содержащая столбец "timestamp"
            (строковые или datetime-совместимые значения).

    Returns:
        pd.DataFrame: Копия таблицы, где столбец "timestamp" приведён к типу datetime64.

    Raises:
        KeyError: Если отсутствует столбец "timestamp".
        ValueError: Если значения в столбце нельзя преобразовать в datetime.
    """

    if "timestamp" not in df.columns:
        raise KeyError("Отсутствует обязательный столбец 'timestamp'.")

    try:
        result = df.copy()

        result["timestamp"] = pd.to_datetime(result["timestamp"], errors="raise")
        return result

    except Exception as e:
        raise ValueError(f"Ошибка преобразования в datetime: {e}")


def extract_parts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Извлечение дня, месяца и года из временной метки.

    Args:
        in_df (pd.DataFrame): Таблица с датами в столбце "timestamp"
            (должен иметь тип datetime64).

    Returns:
        pd.DataFrame: Таблица с новыми столбцами:
        #	- "timestamp" (копия исходного)
            - "day" (день месяца, int)
            - "month" (номер месяца, int)
            - "year" (год, int)
            - "hour" (час, int)
            - "weekday" (день недели, int)
            - "quarter" (квартал, int)
            - "weekday_name" (день недели, str)
            - is_weekend (выходной, int)

    Raises:
        KeyError: Если отсутствует столбец "timestamp".
        TypeError: Если столбец "timestamp" не имеет тип datetime.
    """
    if "timestamp" not in df.columns:
        raise KeyError("Отсутствует обязательный столбец 'timestamp'.")

    if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
        raise TypeError("Столбец 'timestamp' должен быть формата datetime.")

    new_df = pd.DataFrame()

    new_df["day"] = df["timestamp"].dt.day
    new_df["month"] = df["timestamp"].dt.month
    new_df["year"] = df["timestamp"].dt.year
    new_df["hour"] = df["timestamp"].dt.hour

    new_df["quarter"] = df["timestamp"].dt.quarter
    new_df["weekday"] = df["timestamp"].dt.dayofweek

    new_df["weekday_name"] = df["timestamp"].dt.day_name().str[:3]
    new_df["is_weekend"] = new_df["weekday"].isin([5, 6]).astype(int)

    return new_df.copy() 


def display(df: pd.DataFrame, category : List[str], kind : List[str], title : List[str]) -> None:
    '''
        Строит графики по заданным категориям
        :args
              df (pd.DataFrame): Таблица со столбцами (см. extract_parts())
              category (List[str]): Категории, по которым требуется построить график
              kind (List[str]): Типы графиков
              title (List[str]): Названия подграфиков
        :returns
            None
        :raises
            KeyError: Если отсутствует столбец переданных категорий или kind не является доступным вариантом графика.
    '''
    if any(cat not in df.columns for cat in category):
        missing = [cat for cat in category if cat not in df.columns]
        raise KeyError(f"Отсутствуют обязательные столбцы: {missing}")
        
    allowed_kinds = ['line', 'bar', 'barh', 'kde', 'density', 'area', 'hist', 'box', 'pie', 'scatter', 'hexbin']
    if any(k not in allowed_kinds for k in kind):
        not_allowed = [k for k in kind if k not in allowed_kinds]
        raise KeyError(f"Недопустимые типы графиков: {not_allowed}")
    
    fig, axes = plt.subplots(1, len(category), figsize=(5 * len(category), 4))

    if len(category) == 1:
        axes = [axes]
        
    for i in range(len(category)):
        df[category[i]].value_counts().plot(kind=kind[i], ax=axes[i], title=title[i])
    plt.tight_layout()
    plt.show()


def example_main_synthetic() -> None:
    """
    Строит синтетические данные
        :returns
            None
    """
    input_df = create_periodic_dataframe(
        start_timedate_point="2025-09-16 02:35:00",
        periods=15, freq="14h"
    )

    transformed_df = convert_to_datetime(input_df)
    result_df = extract_parts(transformed_df)

    print(result_df)

    display(result_df, ["weekday_name", "weekday_name"], ["bar", "pie"], ["Activity Count by Day of Week", "Days of the week"])


def main_read_file(input_csv : str) -> None:
    """
    Строит таблицу и графики по данным
        :returns
            None
    """
    input_df = load_dataframe_from_file(input_csv)
    transformed_df = convert_to_datetime(input_df)
    result_df = extract_parts(transformed_df)

    print(result_df)
    
    display(result_df, ["weekday_name", "weekday_name"], ["bar", "pie"], ["Activity Count by Day of Week", "Days of the week"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Работа с временными метками (timeseries)."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--example_synthetic",
        action="store_true",
        help="Сгенерировать синтетические временные метки."
    )
    group.add_argument(
        "--file",
        type=str,
        help="Загрузить данные из CSV файла."
    )

    args = parser.parse_args()

    if args.example_synthetic:
        example_main_synthetic()
    elif args.file:
        main_read_file(args.file)
        
