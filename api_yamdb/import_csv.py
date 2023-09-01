import csv
import sqlite3

DATA_BASE = "db.sqlite3"

list_table = [
    {
        "file": "c:/category.csv",
        "table": "reviews_category",
        "fields": "id, name, slug",
        "fields_num": "?,?,?",
    },
    {
        "file": "c:/genre.csv",
        "table": "reviews_genre",
        "fields": "id, name, slug",
        "fields_num": "?,?,?",
    },
    {
        "file": "c:/comments.csv",
        "table": "reviews_comment",
        "fields": "id, review_id, text, author_id, pub_date",
        "fields_num": "?,?,?,?,?",
    },
    {
        "file": "c:/genre_title.csv",
        "table": "reviews_title_genres",
        "fields": "id, title_id, genre_id",
        "fields_num": "?,?,?",
    },
    {
        "file": "c:/titles.csv",
        "table": "reviews_title",
        "fields": "id, name, year, category_id",
        "fields_num": "?,?,?,?",
    },
    {
        "file": "c:/users.csv",
        "table": "reviews_user",
        "fields": "id, username, email, role, bio, first_name, last_name, password, is_superuser, is_staff, is_active, date_joined",
        "fields_num": "?,?,?,?,?,?,?,?,?,?,?,?",
    },
    {
        "file": "c:/review.csv",
        "table": "reviews_review",
        "fields": "id, title_id, text, author_id, rating, pub_date",
        "fields_num": "?,?,?,?,?,?",
    },
]


def import_csv(file, table, fields, fields_num):
    with open(f"{file}", newline="", encoding="UTF8") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            if table == "reviews_user":
                row.extend([1, 0, 0, 1, "2019-09-24 21:08:21.000"])
            try:
                sqlite_connection = sqlite3.connect(DATA_BASE)
                cursor = sqlite_connection.cursor()
                print("Подключен к SQLite")

                sqlite_insert_query = f"""INSERT INTO {table}
                                        ({fields})
                                        VALUES
                                        ({fields_num});"""
                data_tuple = row
                cursor.execute(sqlite_insert_query, data_tuple)
                sqlite_connection.commit()
                print(
                    f"Запись успешно вставлена ​​в таблицу {table} ",
                    cursor.rowcount,
                )
                cursor.close()
            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")


def delete_record(table):
    try:
        sqlite_connection = sqlite3.connect(DATA_BASE)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_delete_query = f"""DELETE from {table}"""
        cursor.execute(sql_delete_query)
        sqlite_connection.commit()
        print(f"В таблице {table} записи успешно удалены")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


for i in range(0, len(list_table)):
    delete_record(list_table[i]["table"])
    import_csv(
        list_table[i]["file"],
        list_table[i]["table"],
        list_table[i]["fields"],
        list_table[i]["fields_num"],
    )
