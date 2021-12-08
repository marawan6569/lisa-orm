import sqlite3
import inspect


class DB:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    def _execute(self, query, params=None):
        if params:
            return self.conn.execute(query, params)

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
        _tables = self._tables()
        if model.get_name() in _tables:
            _query = f"DROP TABLE IF EXISTS '{model.get_name()}';"
            return self._execute(_query)
        else:
            return f'no such table with this name {model.get_name}'

    def save(self, instance):
        _query, _values = instance.get_insert_query()
        cursor = self._execute(_query, _values)
        instance.data['id'] = cursor.lastrowid
        self.conn.commit()

    # Search
    def get(self, model, **kwargs):
        if kwargs:
            _search_query, _params, _fields = model.get_search_query(**kwargs)
            _result = self._execute(_search_query, _params).fetchone()
            if _result:
                _result = dict(zip(_fields, _result))
                return model(**self._get_foreignkey(model, _result))
            else:
                return None
        else:
            print('you should pass field name and its value like:\n\tid=1 ')

    def filter(self, model, **kwargs):

        if kwargs:
            _results = []
            _search_query, _params, _fields = model.get_search_query(**kwargs)
            _result_list = self._execute(_search_query, _params).fetchall()

            if not _result_list:
                return None

            for _result in _result_list:
                _result = dict(zip(_fields, _result))
                _results.append(model(**self._get_foreignkey(model, _result)))

            return _results

        else:
            print('you should pass field name and its value like:\n\tid=1 ')

    def all(self, model):
        _results = []
        _search_query, _fields = model.get_search_query()
        _result_list = self._execute(_search_query).fetchall()

        if not _result_list:
            return None

        for _result in _result_list:
            _result = dict(zip(_fields, _result))
            _results.append(model(**self._get_foreignkey(model, _result)))

        return _results

    def _get_foreignkey(self, model, result_dict: dict):

        for key in result_dict.keys():
            if key.endswith('__id'):
                fk_id = int(result_dict[key])
                fk_model = getattr(model, key[:-4]).model
                fk_value = self.get(fk_model, id=fk_id)
                result_dict.pop(key)
                result_dict[key[:-4]] = fk_value

            else:
                continue

        return result_dict


class Model:
    def __init__(self, **kwargs):
        self.data = {
            'id': None
        }
        for key, value in kwargs.items():
            self.data[key] = value

    def __getattribute__(self, key):
        _data = object.__getattribute__(self, 'data')
        if key in _data:
            return _data[key]
        return object.__getattribute__(self, key)

    @classmethod
    def get_fields(cls):
        _fields = [
            {'id': 'INTEGER PRIMARY KEY AUTOINCREMENT'}
        ]
        members = inspect.getmembers(cls)
        for member in members:
            if isinstance(member[1], Field):
                _fields.append({member[0]: member[1].create_query})

            elif isinstance(member[1], ForeignKey):
                _fields.append({f'{member[0]}__id': member[1].create_query})

        return _fields

    @classmethod
    def get_name(cls):
        if hasattr(cls, 'table_name'):
            return cls.table_name
        return cls.__name__.lower()

    def get_insert_query(self):
        _fields = []
        _values = []
        _placeholders = []
        cls = self.__class__
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Field):
                _fields.append(name)
                _values.append(self.data[name])
                _placeholders.append('?')
            elif isinstance(field, ForeignKey):
                _fields.append(f'{name}__id')
                _values.append(self.data[name].id)
                _placeholders.append('?')

        _insert_query = "INSERT INTO '{table}' ({fields}) VALUES ({placeholders});"\
            .format(table=self.get_name(),
                    fields=", ".join(_fields),
                    placeholders=", ".join(_placeholders))

        return _insert_query, _values

    # Search
    @classmethod
    def get_search_query(cls, **kwargs):
        _fields = ['id']
        _conditions = []
        _params = []
        _search_fields = []

        for key in kwargs.keys():
            if hasattr(cls, key):
                _search_fields.append(key)
            elif key == 'id':
                if type(kwargs['id']) == int:
                    _conditions.append('id=?')
                    _params.append(kwargs['id'])
                else:
                    print('id value must be integer')
                    return None
            elif hasattr(cls, key[:-4]):
                _search_fields.append(key)
            else:
                print(f'{key} is not a field')
                return None

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Field):
                _fields.append(name)
                if name in _search_fields:
                    _conditions.append(f'{name}=?')
                    _params.append(kwargs[name])
            elif isinstance(field, ForeignKey):
                _fields.append(f'{name}__id')
                if name in _search_fields:
                    _conditions.append(f'{name}__id=?')
                    _params.append(kwargs[name].id)
                elif f'{name}__id' in _search_fields:
                    if type(kwargs[f'{name}__id']) == int:
                        _conditions.append(f'{name}__id=?')
                        _params.append(kwargs[f'{name}__id'])
                    else:
                        print('ForeignKey value must be integer')
                        return None

        if kwargs:
            _search_query = "SELECT {fields} FROM '{table_name}' WHERE {conditions};"\
                .format(
                    fields=', '.join(_fields),
                    table_name=cls.get_name(),
                    conditions=' AND '.join(_conditions)
                )

            return _search_query, _params, _fields

        else:
            _search_query = "SELECT {fields} FROM '{table_name}';"\
                .format(
                    fields=', '.join(_fields),
                    table_name=cls.get_name(),
                )
            return _search_query, _fields


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

        self.type = None

    @property
    def create_query(self):
        return f""" {self.type} {self.null} {self.default} {self.unique}""".strip()


# ---------------- Fields -------------------#
class CharField(Field):
    """
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


# relations:
class ForeignKey:
    def __init__(self, model):
        self.model = model

    @property
    def create_query(self):
        return "INTEGER"


if __name__ == '__main__':
    pass
