# encoding=utf-8
from pprint import pprint

from jinja2 import Template


def get_items(data, fields):
    if len(fields) == 0:
        if isinstance(data, list):
            for x in data:
                yield x
        else:
            yield data

        raise StopIteration

    if isinstance(data, dict):
        # Only process if has field
        if fields[0] in data:
            for x in get_items(data[fields[0]], fields[1:]):
                yield x
    elif isinstance(data, list):
        for data_item in data:
            for x in get_items(data_item, fields):
                yield x

    # raise Exception("Could not get data for fields", fields)


class InvalidItemPathError(Exception):
    pass


def transform_item(item, config):
    # pprint(config)
    if 'ifHasField' in config:
        condition_field = config['ifHasField']
        # pprint(item)
        if condition_field in item:
            for field in config['then']:
                value = config['then'][field]

                item[field] = Template(value).render(**item)


def transform(item_config, data):
    for item_path in item_config:
        for config in item_config[item_path]:
            for item in get_items(data, item_path.split('.')):
                # print(item)
                transform_item(item, config)


if __name__ == '__main__':
    data1 = {
        'Page': [
            {
                'formConfig': {
                    'fields': [
                        {'hasMany': 'Area'},
                        {'hasMany': 'User'},
                    ]
                }
            }
        ]
    }

    transform_config = {
        'Page.formConfig.fields': [
            {
                'ifHasField': 'hasMany',
                'then': {
                    'type': 'hasMany',
                    'key': '{{hasMany}}Ids'
                }
            }
        ]
    }
    transform(transform_config, data1)

    pprint(data1)
