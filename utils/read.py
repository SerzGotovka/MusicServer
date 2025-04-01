import sqlite3
import pandas as pd

def read_db(name_db: str) -> dict:
    try:
        with sqlite3.connect(name_db) as conn:
        
            # Получаем названия всех таблиц
            tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
            name_tables = pd.read_sql(tables_query, conn)
            names_list = name_tables['name'].tolist()

    
   
        dataframes = {}

        for name in names_list:
            df = pd.read_sql(f'SELECT * FROM {name}', conn) # Загружаем данные из таблицы и сохраняем в словаре
            dataframes[name] = df  # Сохраняем DataFrame в словаре
            df.to_excel(f'data/{name}.xlsx', index=False)  # Сохраняем в Excel

    except FileNotFoundError:
        print(f'Файл {name_db} не найден')
    except sqlite3.OperationalError as e:
        print(f'Ошибка подключения к базе данных: {e}')
    except pd.io.sql.DatabaseError as e:
        print(f'Ошибка выполнения SQL-запроса: {e}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')

    return dataframes