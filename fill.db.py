import csv
import os
import sqlite3
from sqlite3 import Error

DATA_CSV = (
    'category',
    # 'comments', 'genre', 'genre_title',
    # 'review', 'titles',  # 'users'
)
FIELDS = {
    # 'users', # TODO ТАКОЙ ТАБЛИЦЫ ПОКА НЕТ
    'category': ('id', 'name', 'slug',),
    'comments': ('id', 'review', 'text', 'author', 'pub_date',),
    'genre': ('id', 'name', 'slug',),
    'genre_title': ('id', 'title', 'genre',),  # TODO что за таблица?(в sqlite- есть)
    'review': ('id', 'title_id', 'text', 'author', 'score', 'pub_date',),
    'titles': ('id', 'name', 'year', 'category',),

}

TABLES = {
    'category': 'api_category',
    'comments': 'api_comments',
    'genre': 'api_genre',
    'genre_title': 'api_title_genre',
    'review': 'api_review',
    'titles': 'api_title',
    # 'users': 'users_customuser', # TODO пока не работает(еще нет такой таблицы)
}


def create_connection(db_file):
    """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def fill_tables(conn, table, fields, file):
    """this function may fill the tables"""
    sql = 'INSERT INTO {table}{fields} VALUES{values}'
    cur = conn.cursor()
    with open(file, 'r') as data:
        for line in csv.DictReader(data):
            # cur.execute(sql, task)
            print(line)
        # conn.commit() # TODO на время тестирования!!!


def main():
    """main function"""
    path_dir = os.path.abspath(os.getcwd())
    db = path_dir + 'db.sqlite'
    conn = create_connection(db)
    with conn:
        for file in DATA_CSV:
            table = TABLES.get(file)
            fields = FIELDS.get(file)
            file = path_dir + '/data/' + file + '.csv'
            fill_tables(conn, table, fields, file)
    conn.close()


if __name__ == '__main__':
    main()
