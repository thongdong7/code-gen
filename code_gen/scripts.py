# encoding=utf-8
import logging
from os.path import exists, join

import click

from code_gen.utils.template_utils import generate_all

logging.basicConfig(level=logging.DEBUG)


class InvalidAppDirError(Exception):
    def __str__(self):
        return "Application directory %s does not exists" % self.args[0]


class InvalidTemplateDirError(Exception):
    def __str__(self):
        return "Could not find template directory at %s" % self.args[0]


@click.command(help='Generate')
@click.option('--app-dir', 'app_dir', default='.', help='Application directory. Default is the current directory')
@click.option('--template-dir-name', 'template_dirname', default='template',
              help='Template directory name, default "template"')
def code_gen(app_dir, template_dirname):
    try:
        if not exists(app_dir):
            raise InvalidAppDirError(app_dir)

        template_dir = join(app_dir, template_dirname)
        if not exists(template_dir):
            raise InvalidTemplateDirError(template_dir)

        generate_all(template_dir, output_dir=app_dir)
    except Exception as e:
        print(str(e))
        raise
