# encoding=utf-8
import json
import logging
from copy import copy
from os import walk, makedirs
from os.path import join, relpath, dirname, exists, abspath
from pprint import pprint

import yaml
from jinja2 import Environment
from jinja2.exceptions import UndefinedError

from code_gen.utils.transform_utils import transform

env = Environment()
env.line_statement_prefix = '#'


def to_json(value):
    return json.dumps(value, indent=4, sort_keys=True)


env.filters['tojson'] = to_json


def load_data(path):
    ret = {}
    for root, subdirs, files in walk(path):
        for file_name in files:
            if file_name.startswith('_') or not file_name.endswith('.yml'):
                # Ignore _file and not yaml file
                continue

            template_path = join(root, file_name)
            data = yaml.load(open(template_path))
            ret.update(data)

    return ret


def generate(template_dir, params, output_dir, override=False):
    for root, subdirs, files in walk(template_dir):
        relative_root_dir = relpath(root, template_dir)
        # print(relative_root_dir, root, subdirs, files)
        for file_name in files:
            template_path = join(root, file_name)
            output_template_path = join(output_dir, relative_root_dir, file_name)
            # print(output_template_path)

            output_path = env.from_string(output_template_path).render(**params)
            # print(output_path)

            if exists(output_path) and not _could_override([output_template_path, output_path], override):
                print('Ignore', output_path)
                continue

            tmp_output_dir = dirname(output_path)
            if not exists(tmp_output_dir):
                makedirs(tmp_output_dir)

            template_content = open(template_path).read()
            try:
                content = env.from_string(template_content).render(**params)
            except UndefinedError as e:
                logging.warning('%s: %s' % (template_path, str(e)))
                continue

            open(output_path, 'w').write(content)


def _could_override(paths, override):
    # print(override)
    if isinstance(override, bool):
        return override

    if override is None:
        return False

    if isinstance(override, list):
        for item in override:
            # print(item, path)
            for path in paths:
                if item in path:
                    # print('true')
                    return True

    return False


class TemplateGenerator(object):
    def __init__(self, template_dir, output_dir):
        self.template_dir = template_dir
        self.output_dir = output_dir

    def generate(self):
        params = self._load_params()
        config = self._load_config()
        # pprint(config)

        # Transform params
        self._transform_params(config, params)

        # Generate master
        generate(join(self.template_dir, 'master'),
                 params,
                 output_dir=self.output_dir, override=config.get('override'))

        # Generate item
        for item_name in params:
            item_dir = join(self.template_dir, 'items', item_name)
            if exists(item_dir):
                print('generate', item_name)
                for item_config in params[item_name]:
                    item_params = copy(item_config)
                    item_params['params'] = params

                    generate(template_dir=item_dir,
                             params=item_params,
                             output_dir=self.output_dir, override=config.get('override'))

    def _load_params(self):
        return load_data(join(self.template_dir, 'data'))

    def _load_config(self):
        return yaml.load(open(join(self.template_dir, 'data/_config.yml')))

    def _transform_params(self, config, params):
        transform_config = config.get('transform', {})
        transform(transform_config, params)


def generate_all(template_dir, output_dir):
    template_generator = TemplateGenerator(template_dir, output_dir)
    template_generator.generate()
    # params = load_data(join(template_dir, 'data'))
    #
    # # Generate master
    # generate(join(template_dir, 'master'),
    #          params,
    #          output_dir=output_dir, override=True)
    #
    # # Generate item
    # for item_name in params:
    #     item_dir = join(template_dir, 'items', item_name)
    #     if exists(item_dir):
    #         print('generate', item_name)
    #         for item_config in params[item_name]:
    #             item_params = copy(item_config)
    #             item_params['params'] = params
    #
    #             generate(template_dir=item_dir,
    #                      params=item_params,
    #                      output_dir=output_dir, override=False)


if __name__ == '__main__':
    app_dir = abspath(join(dirname(__file__), "../.."))
    print(app_dir)

    generate_all(join(app_dir, 'template'), output_dir=app_dir)
    # params = load_data(join(app_dir, 'template/data'))
    # generate(join(app_dir, 'template/master'),
    #          params,
    #          output_dir=app_dir)
