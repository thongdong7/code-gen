# encoding=utf-8
import imp
from os.path import join, exists

from zander.utils import yaml_utils


class Macro(object):
    def __init__(self):
        # Install scripts when install dependency
        self.install = []

        # jinja filter
        self.filters = {}

        # Add new vars to jinja global
        self.create_vars = []

        # Change the params before pass to template
        self.params_decors = {}

    def merge(self, other):
        # type: (Macro) -> None
        self.install += other.install
        self.filters.update(other.filters)
        self.create_vars += other.create_vars
        self.params_decors.update(other.params_decors)


class Template(object):
    def __init__(self, path=None):
        self.macro = Macro()

        if path:
            data_dir = join(path, 'data')
            config_file = join(data_dir, '_config.yml')

            if exists(config_file):
                self.config = TemplateConfig(yaml_utils.load(config_file))
            else:
                self.config = TemplateConfig({})

            self.parameters = yaml_utils.load_dir(data_dir)
            self.paths = [path]

            self._load_macros(path, self.macro)
        else:
            self.config = TemplateConfig({})
            self.parameters = {}
            self.paths = []

    def merge(self, template):
        self.config.merge(template.config)
        self.parameters.update(template.parameters)
        self.paths += template.paths

        self.macro.merge(template.macro)

    def _load_macros(self, path, macro):
        if exists(join(path, 'macro/__init__.py')) or exists(join(path, 'macro.py')):
            f, filename, description = imp.find_module('macro', [path])

            template_module = imp.load_module('macro', f, filename, description)
        else:
            return

        create_var_prefix = 'create_var_'
        for item in dir(template_module):
            if item.startswith(create_var_prefix):
                macro.create_vars.append(getattr(template_module, item))

        filter_prefix = 'filter_'
        for item in dir(template_module):
            if item.startswith(filter_prefix):
                filter_name = item[len(filter_prefix):]

                macro.filters[filter_name] = getattr(template_module, item)

        install = getattr(template_module, '_install', None)
        if install:
            macro.install.append(install)

        macro.params_decors = getattr(template_module, 'params_decors', {})


class TemplateConfig(object):
    list_fields = ['override', 'postcmd']

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

    @property
    def postcmd(self):
        return self.data.get('postcmd', [])

    def merge(self, template_config):
        for field in self.list_fields:
            if field not in template_config.data:
                continue

            assert isinstance(template_config.data[field], list)

            if field not in self.data:
                self.data[field] = template_config.data[field]
            else:
                self.data[field] += template_config.data[field]
