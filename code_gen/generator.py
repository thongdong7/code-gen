# encoding=utf-8
from os.path import join, exists

from code_gen.provider.template import TemplateProvider
from code_gen.utils.template_utils import generate


class CodeGenerator(object):
    def __init__(self, path, output_dir):
        self.template = TemplateProvider().get(path)
        self.output_dir = output_dir

        #

    def generate(self):
        params = self.template.parameters

        # Generate master
        self._generate_master(params)

        # TODO Generate items

    def _generate_master(self, params):
        for path in self.template.paths:
            template_dir = join(path, 'master')
            if not exists(template_dir):
                continue

            generate(template_dir=template_dir, params=params, output_dir=self.output_dir,
                     override=self.template.config.override)
