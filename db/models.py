import os
import json
# from lisa_settings import PATH

fields = [
    # {'AutoField': 'It An IntegerField that automatically increments.'},

    {'CharField': 'A field to store text based values.'},
    {'IntegerField': 'It is an integer field.'},
    {'BooleanField', 'A true/false field.'},
    {'FloatField': 'It is a floating-point number represented in Python by a float instance.'},
    {'TextField	': 'A large text field.'},
    {'DateField': 'A date, represented in Python by a datetime.date instance'},
    # {'TimeField	': 'A time, represented in Python by a datetime.time instance.'},
    {'DateTimeField': 'date and time field'},


    {'ForeignKey': 'A many-to-one relationship. Requires two positional arguments:'
                   ' the class to which the model is related and the on_delete option.'},
    
    {'ManyToManyField': 'A many-to-many relationship. Requires a positional argument:'
                        ' the class to which the model is related,'
                        ' which works exactly the same as it does for ForeignKey,'
                        ' including recursive and lazy relationships.'},
    
    {'OneToOneField': 'A one-to-one relationship. Conceptually,'
                      ' this is similar to a ForeignKey with unique=True,'
                      ' but the “reverse” side of the relation will directly return a single object.'},
]


class ModelMeta(type):
    def __new__(mcs, *args, **kwargs):
        lisa_dir = os.getcwd() + '/lisa/'
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

        if os.path.isdir(lisa_dir):
            pass
        else:
            os.mkdir(lisa_dir)
        if os.path.isdir(lisa_dir + 'json/'):
            pass
        else:
            os.mkdir(lisa_dir + 'json/')

        with open(lisa_dir + 'json/' + name + '.json', 'w+') as json_file:
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

        if default is None:
            self.default = ''
        else:
            self.default = f"DEFAULT '{default}'"


# ---------------- Fields -------------------#
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


class IntegerField(Field):
    """
    IntegerField  is an integer field.
    """
    def __init__(self, unique=False, null=False, default=None):
        self.type = "INTEGER"
        super().__init__(unique, null, default)

    def create_query(self):
        return f"""{self.type} {self.null} {self.default} {self.unique}"""


class BooleanField(Field):
    """
    BooleanField is a true/false field.
    """
    def __init__(self):
        self.type = 'BOOLEAN'
        super(BooleanField, self).__init__()

    def create_query(self):
        return f"""{self.type}"""


class FloatField(Field):
    """
    FloatField is a floating-point number represented in Python
     by a float instance.
    """

    def __init__(self, unique=False, null=False, default=None):
        self.type = "FLOAT"
        super().__init__(unique, null, default)

    def create_query(self):
        return f"""{self.type} {self.null} {self.default} {self.unique}"""


class TextField(Field):
    """
    TextField is large text field.
    """

    def __init__(self, unique=False, null=False, default=None):
        self.type = 'TEXT'
        super().__init__(unique, null, default)

    def create_query(self):
        return f""" {self.type} {self.null} {self.default} {self.unique}"""


class DateField(Field):
    """
    DateField is a date, represented in Python by a datetime.date instance
    """

    def __init__(self, unique=False, null=False, default=None, auto_add=False):
        self.type = 'DATE'
        self.auto_add = auto_add
        super().__init__(unique, null, default)

    def create_query(self):
        return f""" {self.type} {self.null} {self.default} {self.unique}"""


class DateTimeField(Field):
    """
    DateTimeField is date and time field
    """

    def __init__(self, unique=False, null=False, default=None, auto_add=False):
        self.type = 'DATETIME'
        self.auto_add = auto_add
        super().__init__(unique, null, default)

    def create_query(self):
        return f""" {self.type} {self.null} {self.default} {self.unique}"""


class TestModel(metaclass=ModelMeta):
    table_name = 'test_model'

    char = CharField(max_length=30, null=True)
    integer = IntegerField(unique=True)
    boolean = BooleanField()
    text = TextField(default='no text')
    date = DateField(auto_add=True)
    datetime = DateTimeField()


class TestModel1(metaclass=ModelMeta):
    table_name = 'test_model_1'

    integer = IntegerField(unique=True)
    boolean = BooleanField()
    datetime = DateTimeField()


class TestModel2(metaclass=ModelMeta):
    table_name = 'test_model_2'

    char = CharField(max_length=30, null=True)
    integer = IntegerField(unique=True)
    boolean = BooleanField()
    date = DateField(auto_add=True)
    datetime = DateTimeField()


class TestModel3(metaclass=ModelMeta):
    table_name = 'test_model_3'

    boolean = BooleanField()
    text = TextField(default='no text')
    date = DateField(auto_add=True)
    datetime = DateTimeField()
