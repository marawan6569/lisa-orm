import os
import sqlite3
from importlib import util

PATH = os.getcwd()
lisa_path = os.getcwd() + '/lisa'
migrations_path = lisa_path + '/migrations/'


if os.path.isdir(migrations_path):
    migrations_files_paths = [file for file in os.listdir(migrations_path)
                              if file[0:4].isnumeric() and not file.endswith('_done.py')]
else:
    migrations_files_paths = []


def import_migrations(file) -> str:
    loc = migrations_path + file
    spec = util.spec_from_file_location(location=loc, name='migrations')
    migration_file = util.module_from_spec(spec)
    spec.loader.exec_module(migration_file)
    return migration_file


def execute_query(sql_query) -> str:
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(sql_query)
    conn.commit()
    conn.close()


def migrate():

    if not migrations_files_paths:
        print('no changes detected')
    else:
        print('-----------' + ' migrating had started. ' + '-----------')
        for migration_file_path in migrations_files_paths:
            print(f'\t[*] start migrating for {migration_file_path}. ')
            migration_file = import_migrations(migration_file_path)
            tables = migration_file.migrations
            tables_name = list(migration_file.migrations.keys())

            for table_name in tables_name:
                print(f'\t\t - getting query for {table_name}.')
                sql_query = tables[table_name]['query']
                execute_query(sql_query)
                print(f'\t\t - executing {table_name} query.')
                print(f'\t\t - {table_name} query executed successfully')
                print('-' * 50)

            print(f'\t[*] {migration_file_path} had migrated successfully.')

            new_name = migration_file_path[0:-3] + '_done.py'
            os.rename(migrations_path + migration_file_path, migrations_path + new_name)

        print('-----------' + ' migrating had finished. ' + '-----------')


if __name__ == '__main__':
    migrate()
