import sqlite3


def __execute(query):
    try:
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return e


def add(model, **kwargs):
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
    insert_query = """INSERT INTO '{}' {} VALUES {};""" \
        .format(model.table_name, fields, values).replace('[', '(') \
        .replace(']', ')')

    cond = __execute(insert_query)
    if cond is not True:
        print('cant adding data cause of ==> ' + str(cond))
        return None
    else:
        print('data added successfully')


def drop(model):
    delete_table_query = f"""DROP TABLE IF EXISTS '{model.table_name}';"""
    delete_fields_from_lisa_table_query = f"""DELETE FROM 'lisa_tables_fields' 
        WHERE field LIKE '%{model.table_name}__%'"""
    cond = __execute(delete_table_query)
    if cond is not True:
        print(f'field to drop {model.table_name} ==>' + str(cond))
        return None
    else:
        print(f'deleted model {model.table_name} successfully')

    cond = __execute(delete_fields_from_lisa_table_query)
    if cond is not True:
        print(f'field to delete {model.table_name} dependencies ==>' + str(cond))
        print(f'\tdelete them manually \n\
        \t\t by deleting all fields that starts with \'{model.table_name}__\' in lisa_tables_fields')
        return None


def delete_field(model, field_name: str):
    """
    BE sure to delete the field from your model to avoid any conflict
    """
    # check if given name is a field
    if field_name not in model.__dict__.keys():
        print(f'{field_name} is not a field.. please write valid field name')
    else:
        # get model fields without field that will be deleted
        model_new_fields = \
            [key for key in model.__dict__.keys() if not key.startswith('__') and key !=
             'table_name' and key != field_name]
        model_new_fields_query = \
            [key + '\' ' + model.__dict__[key].create_query()
             for key in model.__dict__.keys() if not key.startswith('__') and key !=
             'table_name' and key != field_name]
        # rename model to old__model
        rename_old_table = f"""ALTER TABLE '{model.table_name}' RENAME TO 'old__{model.table_name}'"""
        # creating new table with model.table_name
        create_new_table_query = f"""CREATE TABLE '{model.table_name}' {model_new_fields_query};"""\
            .replace('[', "('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, ") \
            .replace(']', ')').replace('",', ',').replace('"', "'").replace("')", ')')
        # get data from old table to new table
        inserting_query = f"INSERT INTO '{model.table_name}' {model_new_fields} " \
            .replace('[', '(').replace(']', ')')
        getting_query = "SELECT {} FROM '{}';".format(', '.join(model_new_fields), f'old__{model.table_name}')
        get_and_insert_query = inserting_query + getting_query
        #  drop old table
        drop_old_table = f"""DROP TABLE 'old__{model.table_name}'"""
        # delete field from lisa_tables_fields
        delete_field_from_lisa = f"DELETE FROM 'lisa_tables_fields'\
        WHERE field IS'{model.table_name}__{field_name}'"

        # executing queries and checking results
        cond = __execute(rename_old_table)
        if cond is not True:
            print(f'cant rename {model.table_name} to old__{model.table_name} cause of' + str(cond))
            return None
        else:
            print(f'Renamed {model.table_name} to old__{model.table_name} successfully')

        cond = __execute(create_new_table_query)
        if cond is not True:
            print(f'cant cant create new {model.table_name} cause of' + str(cond))
            return None
        else:
            print(f'Created new table {model.table_name} successfully')

        cond = __execute(get_and_insert_query)
        if cond is not True:
            print(f'cant move data from {model.table_name} to old__{model.table_name} cause of' + str(cond))
            return None
        else:
            print(f'Inserted data from old__{model.table_name} to {model.table_name} successfully')

        cond = __execute(drop_old_table)
        if cond is not True:
            print(f'cant drop old__{model.table_name} cause of' + str(cond))
            return None
        else:
            print(f'Deleted data from old__{model.table_name} successfully')

        cond = __execute(delete_field_from_lisa)
        if cond is not True:
            print(f'cant delete {field_name} dependencies in lisa_tables_fields\
             cause of' + str(cond) + '\n\tdelete them manually')
            return None
        else:
            print(f'Deleted {model.table_name}__{field_name} from lisa_tables_fields successfully')

        print(f'deleted field {field_name} successfully')
