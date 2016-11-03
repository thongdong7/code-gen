import json

from jinja2 import Environment


def to_json(value):
    return json.dumps(value, indent=4, sort_keys=True)


class Renderer(object):
    def __init__(self):
        self.env = Environment()
        self.env.line_statement_prefix = '##'

        self.add_filter('tojson', to_json)

    def add_macro(self, name, func):
        self.env.globals[name] = func

    def add_filter(self, name, func):
        self.env.filters[name] = func

    def render(self, template, params):
        return self.env.from_string(template).render(**params)
