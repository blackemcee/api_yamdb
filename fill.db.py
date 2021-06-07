import csv
import os
import sqlite3
from sqlite3 import Error

DATA_CSV = (
    'category',
    'comments',
    'genre',
    'genre_title',
    'review',
    'titles',
    'users'
)
FIELDS = {
    'users': ('id', 'username', 'email', 'role', 'description', 'first_name',
              'last_name', 'password', 'is_superuser', 'is_staff', 'bio',),
    'category': ('id', 'name', 'slug',),
    'comments': ('id', 'review_id', 'text', 'author_id', 'pub_date',),
    'genre': ('id', 'name', 'slug',),
    'genre_title': ('id', 'title_id', 'genre_id',),
    'review': ('id', 'title_id', 'text', 'author_id', 'score', 'pub_date',),
    'titles': ('id', 'name', 'year', 'category_id',),

}

TABLES = {
    'category': 'api_category',
    'comments': 'api_comment',
    'genre': 'api_genre',
    'genre_title': 'api_title_genre',
    'review': 'api_review',
    'titles': 'api_title',
    'users': 'users_customuser',
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
    sql = 'INSERT OR IGNORE INTO {table}{fields} VALUES{values}'
    cur = conn.cursor()
    with open(file, 'r', errors="ignore") as data:
        for line in csv.DictReader(data):
            values = tuple(line.values())
            query = sql.format(table=table, fields=fields, values=values)
            # print(query)
            cur.execute(query)
        conn.commit()


def main():
    """main function"""
    path_dir = os.path.abspath(os.getcwd())
    db = path_dir + '/' + 'db.sqlite3'
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
