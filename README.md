# NSU_DA_3_27
## Проект задаёт признак выходной и выводит его на bar plot

Это форк задачи DA-2-07 из https://github.com/qbt29/DA-2-07

## Основные изменения:
* Добавлены новые поля (weekday_name, is_weekend) в extract_parts()
* Изменена функция display() для вывода нескольких подграфиков

## Как запустить:
1. Клонируйте репозиторий:
   ```
   git clone https://github.com/TatianaIl05/NSU_DA_3_27.git
   ```
2. Перейдите в  директорию проекта:
   ```
   cd NSU_DA_3_27
   ```
3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```
4. Установите библиотеку Pandas (если не установлена):
   ```
   pip install pandas
   ```
5. Установите библиотеку Matplotlib (если не установлена):
   ```
    pip install matplotlib
    ```
6. Запустите программу, указав имя загружаемого датафрейма:
    ```
    python change-timeseries.py --file test_database.csv 
    ```

После программа выведет данные и построит 2 графика: bar plot и pie plot

Программа показывает:

* принадлежность дня к выходным
