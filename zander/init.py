# encoding=utf-8
import shutil
from os import makedirs
from os.path import join, dirname, abspath, exists


def generate_template_structure(project_dir):
    project_template_dir = abspath(join(project_dir, 'template'))
    # print('ptd', project_template_dir)
    if exists(project_template_dir):
        return

    current_folder = abspath(dirname(__file__))
    template_folder = join(current_folder, 'data/init_template')
    # print('template folder', template_folder)

    shutil.copytree(template_folder, project_template_dir)

    master_dir = join(project_template_dir, 'master')
    if not exists(master_dir):
        makedirs(master_dir)


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

        generate_template_structure(template_dir)

