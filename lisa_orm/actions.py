import sqlite3
from lisa_orm.test import Test


def _insert(query):
    try:
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()
        return 'data added successfully'
    except Exception as e:
        return e


def add(model=Test, **kwargs):
    fields = []
    values = []
    # getting fields from models
    model_fields = [key for key in model.__dict__.keys() if not key.startswith('__') and key != 'table_name']
    # checking if given kwarg is not field
    for key, value in kwargs.items():
        if key in model_fields:
            fields += [key]
            values += [value]
        else:
            print(f'argument {key} is not field')
            return None

    # create insert query
    insert_query = """INSERT INTO '{}' {} VALUES {};""".format(model.table_name, fields, values).replace('[', '(')\
        .replace(']', ')')
    print(_insert(insert_query))
