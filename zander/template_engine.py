# encoding=utf-8
import json
from os.path import basename

from jinja2 import Environment


class TemplateEngine(object):
    def __init__(self, template, project_dir):
        self.env = Environment()
        self.env.line_statement_prefix = '##'

        def to_json(value):
            return json.dumps(value, indent=4, sort_keys=True)

        self.env.filters['tojson'] = to_json

        self.env.filters.update(template.filters)

        self.env.globals['project_dir'] = project_dir
        self.env.globals['project_name'] = basename(project_dir)

        # Build more vars
        # print(template.filters)
        # print(template.vars_decor)
        params = {}
        for var_name in template.vars_decor:
            var_decor = template.vars_decor[var_name]
            value = var_decor(self.env.globals)
            params[var_name] = value

        # print(params)

        self.env.globals.update(params)

        # print('macros', template.filters)
        # print('lib_name', self.render('{{lib_name}}', abc='a-b-c'))

    @property
    def default_params(self):
        return self.env.globals

    def render(self, content, **params):
        return self.env.from_string(content).render(**params)
