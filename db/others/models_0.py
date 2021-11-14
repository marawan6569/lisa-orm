import os
import sqlite3, json

class ModelMeta(type):
    def __new__(cls, *args, **kwargs):
        migration_folder = os.getcwd() +'/migrations/'
        name = args[0]
        table_name = name
        sql_query = {
            table_name: {

            }
        }
        attrs = dict(args[2])
        for key, value in attrs.items():
            if key.startswith('__') or key == 'table_name':
                pass
            else:
                sql_query[table_name].update({key: value})

        with open(migration_folder + name + '.json', 'w+') as json_file:
            json.dump(sql_query, json_file)
        if os.path.isdir(migration_folder):
            pass
        else:
            os.mkdir(migration_folder)

        return type(*args, **kwargs)

class Field(object):
    def __init__(self, unique: bool = False, null: bool = False, default=None):
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


class CharField(object):
    def __new__(cls, max_length: int, unique: bool = False, null: bool = False, default=None):
        if unique:
            unique = "UNIQUE"
        else:
            unique = ''

        if null:
            null = ''
        else:
            null = 'NOT NULL'

        if default == None:
            default = ''
        else:
            default = f"DEFAULT '{default}'"
        return f"""VARCHAR({max_length}) {null} {default} {unique}"""

class IntegerField(object):
    def __new__(cls, unique: bool = False, null: bool = False, default: int=None):
        if unique:
            unique = "UNIQUE"
        else:
            unique = ''

        if null:
            null = ''
        else:
            null = 'NOT NULL'

        if default == None:
            default = ''
        else:
            default = f"DEFAULT '{default}'"
        return f"""INTEGER {null} {default} {unique}"""

class BooleanField(object):
    def __new__(cls, default:bool=False):
        if default == False:
            default = f"DEFAULT {default}"
        else:
            default = f"DEFAULT {default}"
        return f"""Boolean {default}"""


class ImageField(object):
    def __init__(self, upload_to):
        pass
    def __new__(cls, name):
        pass

    def test(self):
        return 'upload_to'

a = ImageField(upload_to='ss', name='tree')

