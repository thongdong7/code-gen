# encoding=utf-8
from os import walk
from os.path import join

import yaml


def load(path):
    return yaml.load(open(path))


def load_dir(path):
    """
    Load all yaml file in folder

    :param path:
    :type path:
    :return:
    :rtype:
    """
    ret = {}
    for root, subdirs, files in walk(path):
        for file_name in files:
            if file_name.startswith('_') or not file_name.endswith('.yml'):
                # Ignore _file and not yaml file
                continue

            template_path = join(root, file_name)
            data = yaml.load(open(template_path))
            if data:
                ret.update(data)

    return ret


def write(path, data):
    with open(path, 'w') as f:
        f.write(yaml.dump(data))
