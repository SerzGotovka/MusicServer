import sqlite3
import pandas as pd


with sqlite3.connect('chinook.db') as conn:
            # Получаем названия всех таблиц
            tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
            name_tables = pd.read_sql(tables_query, conn)
            names_list = name_tables['name'].tolist()

            dataframes = {}
            for name in names_list:
                df = pd.read_sql(f'SELECT * FROM {name}', conn)  # Загружаем данные из таблицы и сохраняем в словаре
                dataframes[name] = df  # Сохраняем DataFrame в словаре
                df.to_excel(f'data/{name}.xlsx', index=False)  # Сохраняем в Excel

#- Найдите среднюю длительность треков (Milliseconds) в каждом жанре (genres).
tracks_df = dataframes['tracks']
average_duration = tracks_df.groupby('GenreId')['Milliseconds'].mean().round(0).reset_index()
# print(average_duration)


# - Объедините таблицы tracks, albums и artists. Выведите список треков с названием альбома и именем исполнителя в xlsx
tracks_df = dataframes['tracks']
albums_df = dataframes['albums']
artists_df = dataframes['artists']

join_tracks_albums = pd.merge(tracks_df, albums_df, on='AlbumId', how='inner')

total_join = pd.merge(join_tracks_albums, artists_df, on='ArtistId', how='inner')

total_join.rename(columns={
    'Name_x': 'Track_name', 
    'Title': 'Album',  
    'Name_y': 'Artist_name' 
}, inplace=True)

# print(total_join[['Track_name', 'Album', 'Artist_name']])



# - Определите топ-5 самых прибыльных жанров (genres) на основе суммы продаж (invoice_items.UnitPrice * invoice_items.Quantity).

invoice_item_df = dataframes['invoice_items']

print(invoice_item_df)

invoice_item_df