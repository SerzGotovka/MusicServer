import sqlite3
import pandas as pd
from typing import Dict


def load_data_from_db(db_path: str) -> Dict:
    """Загружает данные из базы данных SQLite и сохраняет их в словаре DataFrame."""
    dataframes = {}
    try:
        with sqlite3.connect(db_path) as conn:
            tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
            name_tables = pd.read_sql(tables_query, conn)
            names_list = name_tables["name"].tolist()

            for name in names_list:
                df = pd.read_sql(f"SELECT * FROM {name}", conn)
                dataframes[name] = df
                df.to_excel(f"data/{name}.xlsx", index=False)  # Сохраняем в Excel
    except Exception as e:
        print(f"Ошибка при загрузке данных из базы: {e}")
    return dataframes


def average_track_duration(dataframes: Dict) -> pd.DataFrame:
    """Находит среднюю длительность треков в каждом жанре."""
    try:
        tracks_df = dataframes["tracks"]
        average_duration = (
            tracks_df.groupby("GenreId")["Milliseconds"].mean().round(0).reset_index()
        )
        return average_duration
    except Exception as e:
        print(f"Ошибка при вычислении средней длительности треков: {e}")
        return pd.DataFrame()


def top_genres_by_sales(dataframes: Dict) -> pd.DataFrame:
    """Определяет топ-5 самых прибыльных жанров на основе суммы продаж."""
    try:

        invoice_item_df = dataframes["invoice_items"]

        invoice_item_df["Top_genres"] = (
            invoice_item_df["UnitPrice"] * invoice_item_df["Quantity"]
        )
        top_genres = invoice_item_df.sort_values(by="Top_genres", ascending=False).head(
            5
        )
        return top_genres
    except Exception as e:
        print(f"Ошибка при вычислении топ-5 жанров: {e}")
        return pd.DataFrame()


def top_customers_in_rock(dataframes: Dict) -> pd.DataFrame:
    """Находит клиентов, которые купили больше всего треков в жанре 'Rock'."""
    try:
        tracks_df = dataframes["tracks"]
        genre_df = dataframes["genres"]
        invoice_df = dataframes["invoices"]
        inv_items = dataframes["invoice_items"]

        join_invoice = pd.merge(invoice_df, inv_items, on="InvoiceId", how="inner")
        join_invoice_track = pd.merge(
            join_invoice, tracks_df, on="TrackId", how="inner"
        )
        join_genre = pd.merge(join_invoice_track, genre_df, on="GenreId", how="inner")

        rock_tracks = join_genre[join_genre["Name_y"] == "Rock"]
        rock_customers = (
            rock_tracks.groupby("CustomerId")["Quantity"].sum().reset_index()
        )
        top_rock_customers = rock_customers.sort_values(by="Quantity", ascending=False)
        return top_rock_customers
    except Exception as e:
        print(f"Ошибка при нахождении клиентов, купивших треки в жанре 'Rock': {e}")
        return pd.DataFrame()


def save_report_to_excel(report_data: Dict, file_path: str) -> None:
    """Сохраняет отчет в Excel файл."""
    try:
        with pd.ExcelWriter(file_path) as writer:
            # Создаем Excel файл и сохраняем каждый DataFrame на отдельном листе
            for sheet_name, df in report_data.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    except Exception as e:
        print(f"Ошибка при сохранении отчета в Excel: {e}")


def main():
    db_path = "chinook.db"
    dataframes = load_data_from_db(db_path)

    report_data = {
        "Average Track Duration": average_track_duration(dataframes),
        "Top Genres by Sales": top_genres_by_sales(dataframes),
        "Top Customers in Rock": top_customers_in_rock(dataframes),
    }

    # Сохраняем отчет в Excel файл
    save_report_to_excel(report_data, "report.xlsx")


if __name__ == "__main__":
    main()
