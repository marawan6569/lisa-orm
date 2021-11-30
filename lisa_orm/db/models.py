# import os
# import json
import sqlite3
import inspect


# fields = [
#     # {'AutoField': 'It An IntegerField that automatically increments.'},
#
#     {'CharField': 'A field to store text based values.'},
#     {'IntegerField': 'It is an integer field.'},
#     {'BooleanField', 'A true/false field.'},
#     {'FloatField': 'It is a floating-point number represented in Python by a float instance.'},
#     {'TextField	': 'A large text field.'},
#     {'DateField': 'A date, represented in Python by a datetime.date instance'},
#     # {'TimeField	': 'A time, represented in Python by a datetime.time instance.'},
#     {'DateTimeField': 'date and time field'},
#
#
#     {'ForeignKey': 'A many-to-one relationship. Requires two positional arguments:'
#                    ' the class to which the model is related and the on_delete option.'},
#
#     {'ManyToManyField': 'A many-to-many relationship. Requires a positional argument:'
#                         ' the class to which the model is related,'
#                         ' which works exactly the same as it does for ForeignKey,'
#                         ' including recursive and lazy relationships.'},
#
#     {'OneToOneField': 'A one-to-one relationship. Conceptually,'
#                       ' this is similar to a ForeignKey with unique=True,'
#                       ' but the “reverse” side of the relation will directly return a single object.'},
# ]


# class ModelMeta(type):
#     def __new__(mcs, *args, **kwargs):
#         lisa_dir = os.getcwd() + '/lisa/'
#         name = args[0]
#         table_name = args[2]['table_name']
#         sql_query = {
#             table_name: {
#
#             }
#         }
#         lisa_table = 'lisa_tables_fields'
#         lisa_table_sql_query = f"""CREATE TABLE  IF NOT EXISTS '{lisa_table}'(
#             'field' VARCHAR(50) NOT NULL UNIQUE,
#              'type' VARCHAR(30) NOT NULL,
#              'is_null' BOOLEAN,
#              'is_unique' BOOLEAN,
#              'default' TEXT,
#              'max_length' INTEGER
#          ); """
#         conn = sqlite3.connect('db.sqlite3')
#         cur = conn.cursor()
#         cur.execute(lisa_table_sql_query)
#         conn.commit()
#         conn.close()
#         attrs = dict(args[2])
#         for key, value in attrs.items():
#             if isinstance(key, Field):
#                 sql_query[table_name].update({key: value.create_query().strip()})
#
#                 field_name = key
#                 field_type = value.type
#                 if value.null == 'NOT NULL':
#                     is_null = 0
#                 else:
#                     is_null = 1
#                 if value.unique == 'UNIQUE':
#                     is_unique = 1
#                 else:
#                     is_unique = 0
#                 default_value = value.default
#                 if hasattr(value, 'max_length'):
#                     max_len = value.max_length
#                     q = f"""INSERT INTO '{lisa_table}'
#                         ('field', 'type', 'is_null', 'is_unique', 'default', 'max_length')
#                         VALUES
#                         ('{table_name}__{field_name}', '{field_type}', {is_null}, {is_unique}, '{default_value}',
#                         {max_len});"""
#                 else:
#                     q = f"""INSERT INTO '{lisa_table}'
#                         ('field', 'type', 'is_null', 'is_unique', 'default')
#                         VALUES
#                         ('{table_name}__{field_name}', '{field_type}', {is_null}, {is_unique}, '{default_value}');"""
#                 try:
#                     conn = sqlite3.connect('db.sqlite3')
#                     cur = conn.cursor()
#                     cur.execute(q)
#                     conn.commit()
#                     conn.close()
#                 except sqlite3.IntegrityError:
#                     pass
#         if os.path.isdir(lisa_dir):
#             pass
#         else:
#             os.mkdir(lisa_dir)
#         if os.path.isdir(lisa_dir + 'json/'):
#             pass
#         else:
#             os.mkdir(lisa_dir + 'json/')
#
#         with open(lisa_dir + 'json/' + name + '.json', 'w+') as json_file:
#             json.dump(sql_query, json_file)
#
#         return type(*args, **kwargs)


class DB:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    def _execute(self, query):
        return self.conn.execute(query)

    def _tables(self):
        _query = "SELECT name FROM sqlite_master WHERE type = 'table';"

        _tables = [table[0] for table in self._execute(_query).fetchall()]
        return _tables

    def create(self, model):
        _fields = []
        for field in model.get_fields():
            _fields.append(f"'{list(field.keys())[0]}' {list(field.values())[0]}")
        _fields = ", ".join(_fields)
        _query = f"CREATE TABLE IF NOT EXISTS '{model.get_name()}' ({_fields});"
        self._execute(_query)

    def drop(self, model):
        _query = f"DROP TABLE IF EXISTS '{model.get_name()}';"
        return self._execute(_query)


class Model:
    def __init__(self, **kwargs):
        pass

    @classmethod
    def get_fields(cls):
        _fields = []
        members = inspect.getmembers(cls)
        for member in members:
            if isinstance(member[1], Field):
                _fields.append({member[0]: member[1].create_query})

        return _fields

    @classmethod
    def get_name(cls):
        if hasattr(cls, 'table_name'):
            return cls.table_name
        return cls.__name__.lower()


class Field(object):
    def __init__(self, unique=False, null=False, default=None):

        if unique:
            self.unique = "UNIQUE"
        else:
            self.unique = ''

        if null:
            self.null = ''
        else:
            self.null = 'NOT NULL'

        if default is None:
            self.default = ''
        else:
            self.default = f"DEFAULT '{default}'"

    @property
    def create_query(self):
        return f""" {self.type} {self.null} {self.default} {self.unique}""".strip()


# ---------------- Fields -------------------#
class CharField(Field):
    """"
    CharField is A field to store text based values.
    """

    def __init__(self, max_length, unique=False, null=False, default=None):

        self.max_length = max_length
        self.type = f'VarChar({max_length})'
        super().__init__(unique, null, default)


class IntegerField(Field):
    """
    IntegerField  is an integer field.
    """
    def __init__(self, unique=False, null=False, default=None):
        self.type = "INTEGER"
        super().__init__(unique, null, default)


class BooleanField(Field):
    """
    BooleanField is a true/false field.
    """
    def __init__(self):
        self.type = 'BOOLEAN'
        super(BooleanField, self).__init__()

    @property
    def create_query(self):
        return f"""{self.type}""".strip()


class FloatField(Field):
    """
    FloatField is a floating-point number represented in Python
     by a float instance.
    """

    def __init__(self, unique=False, null=False, default=None):
        self.type = "FLOAT"
        super().__init__(unique, null, default)


class TextField(Field):
    """
    TextField is large text field.
    """

    def __init__(self, unique=False, null=False, default=None):
        self.type = 'TEXT'
        super().__init__(unique, null, default)


class DateField(Field):
    """
    DateField is a date, represented in Python by a datetime.date instance
    """

    def __init__(self, unique=False, null=False, default=None, auto_add=False):
        self.type = 'DATE'
        self.auto_add = auto_add
        super().__init__(unique, null, default)


class DateTimeField(Field):
    """
    DateTimeField is date and time field
    """

    def __init__(self, unique=False, null=False, default=None, auto_add=False):
        self.type = 'DATETIME'
        self.auto_add = auto_add
        super().__init__(unique, null, default)


if __name__ == '__main__':
    pass
