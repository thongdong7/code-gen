# encoding=utf-8
from os.path import join

from code_gen.utils import yaml_utils


class TemplateConfig(object):
    def __init__(self, data):
        self.data = data

        assert 'override' in data or isinstance(data['override'], list)

    @property
    def override(self):
        return self.data.get('override', [])


class Template(object):
    def __init__(self, path):
        data_dir = join(path, 'data')
        config_file = join(data_dir, '_config.yml')

        self.config = TemplateConfig(yaml_utils.load(config_file))
        self.parameters = yaml_utils.load_dir(data_dir)

        self.path = path

    def merge(self, template):
        self.config.merge(template.config)
        self.parameters.update(template.parameters)
