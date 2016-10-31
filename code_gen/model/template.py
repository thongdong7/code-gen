# encoding=utf-8
from os.path import join, exists

from code_gen.utils import yaml_utils


class Template(object):
    def __init__(self, path=None):
        if path:
            data_dir = join(path, 'data')
            config_file = join(data_dir, '_config.yml')

            if exists(config_file):
                self.config = TemplateConfig(yaml_utils.load(config_file))
            else:
                self.config = TemplateConfig({})

            self.parameters = yaml_utils.load_dir(data_dir)
            self.paths = [path]
        else:
            self.config = TemplateConfig({})
            self.parameters = {}
            self.paths = []

    def merge(self, template):
        self.config.merge(template.config)
        self.parameters.update(template.parameters)
        self.paths += template.paths


class TemplateConfig(object):
    list_fields = ['override']

    def __init__(self, data):
        self.data = data

        assert 'override' not in data or isinstance(data['override'], list)

    @property
    def override(self):
        return self.data.get('override', [])

    def merge(self, template_config):
        for field in self.list_fields:
            if field not in template_config.data:
                continue

            assert isinstance(template_config.data[field], list)

            if field not in self.data:
                self.data[field] = template_config.data[field]
            else:
                self.data[field] += template_config.data[field]
