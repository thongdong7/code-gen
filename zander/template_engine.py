# encoding=utf-8
import json
from os.path import basename
import pprint
from jinja2 import Environment


class TemplateEngine(object):
    def __init__(self, template, project_dir):
        self.macro = template.macro
        self.env = Environment(
            extensions=['jinja2.ext.do']
        )
        self.env.line_statement_prefix = '##'

        def to_json(value):
            return json.dumps(value, indent=4, sort_keys=True)

        def _pprint(value, margin=0):
            return pprint.pformat(value, indent=2).replace('\n', '\n' + ' ' * margin)

        self.env.filters['tojson'] = to_json
        self.env.filters['pprint'] = _pprint

        self.env.filters.update(self.macro.filters)

        self.env.globals['project_dir'] = project_dir
        self.env.globals['project_name'] = basename(project_dir)

        # Register filter

    @property
    def default_params(self):
        return self.env.globals

    def decor_params(self, params):
        # decor
        for param_name in self.macro.params_decors:
            # print(param_name)
            param_decor_method = self.macro.params_decors[param_name]
            params[param_name] = param_decor_method(params[param_name])

        # create var
        for method in self.macro.create_vars:
            params.update(method(params))

        return params

    def render(self, content, **params):
        return self.env.from_string(content).render(**params)
