# encoding=utf-8
import imp
from os.path import join, exists

from zander.utils import yaml_utils


class Template(object):
    def __init__(self, path=None):
        self.filters = {}
        self.vars_decor = {}
        self.install = None
        if path:
            data_dir = join(path, 'data')
            config_file = join(data_dir, '_config.yml')

            if exists(config_file):
                self.config = TemplateConfig(yaml_utils.load(config_file))
            else:
                self.config = TemplateConfig({})

            self.parameters = yaml_utils.load_dir(data_dir)
            self.paths = [path]

            macro_file = join(path, 'template.py')
            if exists(macro_file):
                self.install, self.filters, self.vars_decor = self._load_macros(macro_file)
        else:
            self.config = TemplateConfig({})
            self.parameters = {}
            self.paths = []

    def merge(self, template):
        self.config.merge(template.config)
        self.parameters.update(template.parameters)
        self.paths += template.paths
        self.filters.update(template.filters)
        self.vars_decor.update(template.vars_decor)

    def _load_macros(self, macro_file):
        macro = imp.load_source('macro', macro_file)
        install = getattr(macro, '_install', None)
        filters = getattr(macro, 'filters', {})
        vars_decor = getattr(macro, 'vars_decor', {})

        return install, filters, vars_decor


class TemplateConfig(object):
    list_fields = ['override']

    def __init__(self, data):
        if not data:
            self.data = {}
        else:
            self.data = data

        assert 'override' not in self.data or isinstance(self.data['override'], list)

    @property
    def override(self):
        return self.data.get('override', [])

    @override.setter
    def override(self, value):
        self.data['override'] = value

    def merge(self, template_config):
        for field in self.list_fields:
            if field not in template_config.data:
                continue

            assert isinstance(template_config.data[field], list)

            if field not in self.data:
                self.data[field] = template_config.data[field]
            else:
                self.data[field] += template_config.data[field]
