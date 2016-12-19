# encoding=utf-8
import json

from jinja2 import Environment


class TemplateEngine(object):
    def __init__(self, template):
        self.env = Environment()
        self.env.line_statement_prefix = '##'

        def to_json(value):
            return json.dumps(value, indent=4, sort_keys=True)

        self.env.filters['tojson'] = to_json

        self.env.globals.update(template.macros)

    def render(self, content, **params):
        return self.env.from_string(content).render(**params)
