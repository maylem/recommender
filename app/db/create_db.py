import csv
import os
import sqlite3


def insert_data(conn, table_name, table_desc, file_path):
    """
    Populate an existing table with data from a given file.
    :param conn: sqlite db connection
    :param table_name: string, table name
    :param table_desc: Dict, keys are table names and values are lists of column name and data type tuples
    :param file_path: string, directory path to data file needed for data inserts
    """
    c = conn.cursor()

    with open(file_path, 'r') as data:
        row_gen = csv.DictReader(data)

        for row in row_gen:
            to_insert = tuple(row[col] for (col, _) in table_desc)
            c.execute('INSERT INTO {t}'.format(t=table_name) + ' ' + str(tuple(col for (col, _) in table_desc)) +
                      ' VALUES ' + str(to_insert) + ';')


def create_table(conn, table_name, table_desc):
    """
    Drop existing tables and create new tables with the specified names and column types.
    :param conn: sqlite db connection
    :param table_name: string, table name
    :param table_desc: Dict, keys are table names and values are lists of column name and data type tuples
    """
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS {t}'.format(t=table_name))
    columns = '(' + ', '.join(col + ' ' + col_type for (col, col_type) in table_desc) + ')'
    c.execute('CREATE TABLE {t} {cols};'.format(t=table_name, cols=columns))


def files_exist(data_files):
    """
    Determine whether each file in the given path list exists.
    :param data_files: List of file path strings
    :return: List of boolean values representing whether a file exists in its specified path
    """
    file_exists = []

    for data_file in data_files:
        file_exists.append(os.path.exists(data_file))

    return file_exists


def create_db(db_path, file_paths, table_desc):
    """
    Create and populate tables from existing data files. If a needed data file is missing, raise a FileNotFoundError.
    :param db_path: string, directory path to .sqlite db file
    :param file_paths: list of string directory paths to data files needed for db creation
    :param table_desc: Dict, keys are table names and values are lists of column name and data type tuples
    :return: sqlite db connection if the db was successfully created
    """
    files_exist_mask = files_exist(file_paths)

    if all(files_exist_mask):
        conn = sqlite3.connect(db_path)

        for data_file in file_paths:
            table_name = data_file.split('/', 1)[-1].split('.', 1)[0]

            create_table(conn, table_name=table_name, table_desc=table_desc[table_name])
            insert_data(conn, table_name=table_name, table_desc=table_desc[table_name], file_path=data_file)

        conn.commit()
        return conn
    else:
        raise FileNotFoundError('Missing file(s) ' + ''.join(
            data_file for (i, data_file) in enumerate(file_paths) if not files_exist_mask[i]))
