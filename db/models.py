import os
import sqlite3, traceback, json
from lisa_settings import PATH

fields = [
    {'CharField': 'A field to store text based values.'},
    {'IntegerField': 'It is an integer field.'},
    {'BooleanField', 'A true/false field.'},
    {'AutoField': 'It An IntegerField that automatically increments.'},
    {'FloatField': 'It is a floating-point number represented in Python by a float instance.'},
    {'TextField	': 'A large text field. The default form widget for this field is a Textarea.'},
    {'DateField': 'A date, represented in Python by a datetime.date instance'},
    {'TimeField	': 'A time, represented in Python by a datetime.time instance.'},
    {'DateTimeField': 'date and field'},
    {'ForeignKey': 'A many-to-one relationship. Requires two positional arguments: the class to which the model is related and the on_delete option.'},
    {'ManyToManyField': 'A many-to-many relationship. Requires a positional argument: the class to which the model is related, which works exactly the same as it does for ForeignKey, including recursive and lazy relationships.'},
    {'OneToOneField': 'A one-to-one relationship. Conceptually, this is similar to a ForeignKey with unique=True, but the “reverse” side of the relation will directly return a single object.'},
]

class ModelMeta(type):
    def __new__(cls, *args, **kwargs):
        migration_folder = os.getcwd() +'/migrations/'
        name = args[0]
        table_name = args[2]['table_name'] or name
        sql_query = {
            table_name: {

            }
        }
        attrs = dict(args[2])
        for key, value in attrs.items():
            if key.startswith('__') or key == 'table_name':
                pass
            else:
                sql_query[table_name].update({key: value.create_query().strip()})


        if os.path.isdir(migration_folder):
            pass
        else:
            os.mkdir(migration_folder)

        with open(migration_folder + name + '.json', 'w+') as json_file:
            json.dump(sql_query, json_file)

        return type(*args, **kwargs)

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

        if default == None:
            self.default = ''
        else:
            self.default = f"DEFAULT '{default}'"

        if True:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
        self.__column_name__ = def_name

    def create_query(self):
        return f""" {self.type} {self.null} {self.default} {self.unique}"""


    def __name__(self):
        return self.__column_name__


class CharField(Field):
    """"
    CharField is A field to store text based values.
    """

    def __init__(self, max_length, unique=False, null=False, default=None):

        self.max_length = max_length
        self.type = f'VarChar({max_length})'
        super().__init__(unique, null, default)

    def create_query(self):
        return f""" {self.type} {self.null} {self.default} {self.unique}"""


class Test(metaclass=ModelMeta):
    table_name = 'marwan'
    field1 = CharField(max_length=10,)