# encoding=utf-8
from os.path import join

from code_gen.utils import yaml_utils


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


class TemplateConfig(object):
    list_fields = ['override']

    def __init__(self, data):
        self.data = data

        assert 'override' in data or isinstance(data['override'], list)

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
