import json
import os

lisa_dir = os.getcwd() + '/lisa/'
migrations_dir = lisa_dir + '/migrations/'
json_dir = lisa_dir + '/json'


def make_migrations():
    if os.path.isdir(json_dir) and os.listdir(json_dir) != []:
        if os.path.isdir(lisa_dir):
            if os.path.isdir(migrations_dir):
                pass
            else:
                os.mkdir(migrations_dir)
        else:
            os.mkdir(lisa_dir)
            os.mkdir(migrations_dir)

        migrations_files = os.listdir(migrations_dir)
        header = '''"""
    - Lisa ORM version 0.0
    - author: Marwan Mohamed
    - github: https://github.com/marawan6569/
     - facebook: https://www.facebook.com/marwanmo7amed8
    - twitter: https://twitter.com/Marwan_Mo7amed_ 
    - instagram: https://www.instagram.com/marwan_mohamed_0_0/
    """'''

        if not migrations_files:
            current_migration_file = '0001_initial.py'
        else:
            migrations_files = [file for file in migrations_files if file[0:4].isnumeric()]
            migrations_files = sorted(migrations_files)
            current_migration_file = str(int(migrations_files[-1][0:4]) + 1).zfill(4) + '_migration.py'

        with open(migrations_dir + current_migration_file, 'w+') as migrations_file:
            migrations_file.writelines(header + '\n\nmigrations = {')

        if os.path.isdir(json_dir):
            tables = list(os.listdir(json_dir))
            if tables is not None:

                for table in tables:
                    sql_query = f"""\t\t\tCREATE TABLE IF NOT EXISTS  """
                    if table.endswith('.json'):
                        with open(json_dir + '/' + table, 'r') as json_file:
                            query = json.load(json_file)
                            table_name = list(query.keys())[0]
                            fields = query[table_name]
                            sql_query += f"'{table_name}'(\n\t\t\t\t'id'" \
                                         f" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,\n"

                            for field_name, field_query in fields.items():

                                sql_query += f"\t\t\t\t'{field_name}' {field_query},\n"
                            sql_query = sql_query[0:-2]
                            sql_query += "\n\t\t\t);"

                            migration_query = '''	
    "{}": {}
        "status": "creating", 
        "query": """\n{}"""
        {},\n'''.format(table_name, '{', sql_query, '}')
                            with open(migrations_dir + current_migration_file, 'a') as migrations_file:
                                migrations_file.writelines(migration_query)
                            # print(sql_query)
                            os.remove(lisa_dir + '/json/' + table)
                    else:
                        pass

                with open(migrations_dir + current_migration_file, 'a') as migrations_file:
                    migrations_file.write('}\n')
            else:
                print('No changes detected.\nif you made some changes please be sure to run models.py')
        else:
            print('No changes detected.\nif you made some changes please be sure to run models.py')
    else:
        print('No changes detected.\nif you made some changes please be sure to run models.py')


if __name__ == '__main__':
    make_migrations()
