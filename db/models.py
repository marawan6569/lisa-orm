import sqlite3, traceback


class Model:
    def __init__(self, path):
        db_connection = sqlite3.connect(path)
        db_cursor = db_connection.cursor()


        def_name = None
        if def_name == None:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
        self.__table_name__ = def_name

    def __name__(self):
        return self.__table_name__


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

        def_name = None
        if def_name == None:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
        self.__field_name__ = def_name


    def __name__(self):
        return self.__field_name__

class  TestField(Field):
    def __init__(self, table, unique=False, null=False, default=None):
        super().__init__(table, unique, null, default,)
        def_name = None
        if def_name == None:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
        self.__field_name__ = def_name

    def create_query(self):
        self.type = 'TEST'
        print(f"""'{self.__field_name__}' {self.type} {self.null} {self.default} {self.unique},""")

class CharField(Field):

    def create_query(self):
        self.type = 'TEXT'
        print(f"""'{self.__field_name__}' {self.type} {self.null} {self.default} {self.unique},""")

class IntegerField(Field):

    def create_query(self):
        self.type = 'INTEGER'
        print(f"""'{self.__field_name__}' {self.type} {self.null} {self.default} {self.unique},""")

class ImageField(Field):

    def __init__(self, table, upload_to, unique=False, null=False, default=None):
        super().__init__(table, unique, null, default)

        self.upload_to = upload_to

        def_name = None
        if def_name == None:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
        self.__field_name__ = def_name

    def create_query(self):
        self.type = 'TEXT'
        print(f"""'{self.__field_name__}' {self.type} {self.null} {self.default} {self.unique},""")

    def upload(self, image_source):
        pass

class FileField(Field):
    def __init__(self, table, upload_to, unique=False, null=False, default=None):
        super().__init__(table, unique, null, default)

        self.upload_to = upload_to

        def_name = None
        if def_name == None:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
        self.__field_name__ = def_name

    def create_query(self):
        self.type = 'TEXT'
        print(f"""'{self.__field_name__}' {self.type} {self.null} {self.default} {self.unique},""")

    def upload(self, image_source):
        pass


test = ImageField(table='f', upload_to='', unique=True, default='gg')
test1 = ImageField(table='f', upload_to='', unique=True, default='gg')
test2 = ImageField(table='f', upload_to='', unique=True, default='gg')
print(test.__name__())
print(test1.__name__())
print(test2.__name__())

test.create_query()
test1.create_query()
test2.create_query()