# encoding=utf-8
import shutil
from os.path import pardir, join, dirname, abspath, exists

from os import makedirs


class InitTemplate(object):
    def __init__(self, template_name, app_dir):
        self.app_dir = app_dir
        self.template_name = template_name

        current_folder = abspath(dirname(__file__))
        self._template_folder = join(current_folder, 'data/init_template')

        self._workspace_dir = join(app_dir, '.code-gen')

    def execute(self):
        if not exists(self._workspace_dir):
            makedirs(self._workspace_dir)

        template_dir = join(self._workspace_dir, self.template_name)
        if exists(template_dir):
            print('%s existed' % self.template_name)
            return

        shutil.copytree(self._template_folder, template_dir)
        master_dir = join(template_dir, 'master')
        if not exists(master_dir):
            makedirs(master_dir)

