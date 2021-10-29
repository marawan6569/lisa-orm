import os
import sqlite3, traceback, json
from lisa_settings import PATH

from django.db import migrations
class Model:

    def __init__(self):

        global json_file_path
        table_name = ''
        json_file_path = PATH + '/' + f'migrations/{self.table_name}.json'
        self.json_file_path = json_file_path
        self.DB_path = PATH + '/' + 'db.sqlite3'

        # getting instance name
        if True:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
        self.__table_name__ = def_name

        self.name_in_db = self.__table_name__

    def __name__(self):
        return self.__table_name__

    def make_migrations(self):
        table_json = {
            f'{self.table_name}':
                {
                    'Fields': []
                }
        }
        if os.path.isdir(PATH+'/migrations/'):
            pass
        else:
            os.mkdir(PATH+'/migrations/')
        with open(json_file_path, 'w+') as json_file:
            json.dump(table_json, json_file)

    def migrate(self):
        pass
        with open(self.json_file_path, 'r') as json_file:
            fields = json.load(json_file)
            fields = ', '.join(fields[f'{self.table_name}']['Fields'])

            sql_query = "CREATE TABLE IF NOT EXISTS "\
                        + self.table_name + "(" \
                        + fields + ")"
            with sqlite3.connect(self.DB_path) as connection:
                cursor = connection.cursor()
                cursor.execute(sql_query)
                connection.commit()
                print('done')

class Field:
    def __init__(self, table, unique=False, null=False, default=None):
        self.table = table

        if unique:
            self.unique = "UNIQUE"
        else:
            self.unique = ''

        if null:
            self.null = ''
        else:
            self.null = 'NOT NULL'

        if default == None:
            self.default = ''
        else:
            self.default = f"DEFAULT '{default}'"

        if True:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
        self.__column_name__ = def_name

    def make_migrations(self):
        self.query = f"""'{self.__column_name__}' {self.type} {self.null} {self.default} {self.unique}"""

        with open(json_file_path, 'r') as json_file:
            table = json.load(json_file)
            table[f'{self.table}']['Fields'] += [self.query]
            with open(json_file_path, 'w') as json_file:
                json.dump(table, json_file)


    def __name__(self):
        return self.__column_name__



class CharField(Field):
    def __init__(self, table, unique=False, null=False, default=None):
        """

        :rtype: object
        """
        self.type = 'TEXT'
        super().__init__(table, unique, null, default)


        # getting Field name
        if True:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
        self.__column_name__ = def_name

class IntegerField(Field):
    def __init__(self, table, unique=False, null=False, default=None):
        self.type = 'INTEGER'
        super().__init__(table, unique, null, default)


        # getting Field name
        if True:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
        self.__column_name__ = def_name

class ImageField(Field):
    def __init__(self, table, upload_to, unique=False, null=False, default=None):
        self.type = 'TEXT'
        super().__init__(table, unique, null, default)

        self.upload_to = upload_to

        if True:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
        self.__column_name__ = def_name

    def upload(self, image_source):
        pass

class FileField(Field):
    def __init__(self, table, upload_to, unique=False, null=False, default=None):
        self.type = 'TEXT'
        super().__init__(table, unique, null, default)

        self.upload_to = upload_to

        if True:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
        self.__column_name__ = def_name

    def upload(self, image_source):
        pass