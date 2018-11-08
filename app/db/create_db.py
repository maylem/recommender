import csv
import os
import sqlite3


def insert_data(conn, table_name, table_desc, file_path):
    c = conn.cursor()

    with open(file_path, 'r') as data:
        row_gen = csv.DictReader(data)

        for row in row_gen:
            to_insert = tuple(row[col] for (col, _) in table_desc)
            c.execute('INSERT INTO ' + table_name + ' ' + str(tuple(col for (col, _) in table_desc)) +
                      ' VALUES ' + str(to_insert) + ';')


def create_table(conn, table_name, table_desc):
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS ' + table_name)
    columns = '(' + ', '.join(col + ' ' + col_type for (col, col_type) in table_desc) + ')'
    c.execute('CREATE TABLE {t} {cols};'.format(t=table_name, cols=columns))


def files_exist(data_files):
    file_exists = []

    for data_file in data_files:
        file_exists.append(os.path.exists(data_file))

    return file_exists


def create_db(db_path, file_paths, table_desc):
    files_exist_mask = files_exist(file_paths)

    if all(files_exist_mask):
        conn = sqlite3.connect(db_path)

        for data_file in file_paths:
            table_name = data_file.split('/', 1)[-1].split('.', 1)[0]

            create_table(conn, table_name=table_name, table_desc=table_desc[table_name])
            insert_data(conn, table_name=table_name, table_desc=table_desc[table_name], file_path=data_file)

        conn.commit()
        conn.close()
    else:
        raise FileNotFoundError('Missing file(s) ' + ''.join(
            data_file for (i, data_file) in enumerate(file_paths) if not files_exist_mask[i]))
