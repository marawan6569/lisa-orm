import sqlite3
import json


def __execute(query, one=False):
    try:
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        data = cur.execute(query)
        if not one:
            data = data.fetchall()
        else:
            data = data.fetchone()
        conn.close()
        return data

    except Exception as e:
        return e


def __to_json(result, fields, one=False):
    if not one:
        json_obj = []
        for res_list in result:
            row = {}
            for index, res in enumerate(res_list):
                row.update({fields[index]: res})

            json_obj.append(row)
    else:
        json_obj = {}
        for index, res in enumerate(result):
            json_obj.update({fields[index]: res})
    return json.dumps(json_obj)


def __to_dict(result, fields, one=False):
    if not one:
        dict_obj = []
        for res_list in result:
            row = {}
            for index, res in enumerate(res_list):
                row.update({fields[index]: res})

            dict_obj.append(row)

    else:
        dict_obj = {}
        for index, res in enumerate(result):
            dict_obj.update({fields[index]: res})

    return dict_obj


def get_all(model, export_to_json: bool = False):
    # getting fields from model
    fields = [key for key in model.__dict__.keys()
              if not key.startswith('__') and key != 'table_name']
    fields.insert(0, 'id')

    # creating search query
    search_query = f"SELECT {', '.join(fields)} FROM '{model.table_name}';"\

    # getting result from db
    result = __execute(search_query)
    if result != list:
        if export_to_json:
            return __to_json(result, fields)

        else:
            return __to_dict(result, fields)

    else:
        return result


def get(model, export_to_json: bool = False, **kwargs):
    # TODO: add WHERE condition
    # getting fields from model
    fields = [key for key in model.__dict__.keys()
              if not key.startswith('__') and key != 'table_name']
    fields.insert(0, 'id')

    # creating search query
    search_query = f"SELECT {', '.join(fields)} FROM '{model.table_name}';"\

    # getting result from db
    result = __execute(search_query, one=True)
    if result != list:
        if export_to_json:
            return __to_json(result, fields, one=True)

        else:
            return __to_dict(result, fields, one=True)

    else:
        return result

