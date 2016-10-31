# encoding=utf-8
from code_gen.model.template import Template


class CodeGenerator(object):
    def __init__(self):
        self.master_template = Template()

    def add(self, template):
        self.master_template.merge(template)

    def generate(self):
        pass
