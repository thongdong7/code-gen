import shlex
import subprocess
from os import makedirs, symlink, unlink
from os.path import join, exists, pardir, abspath

from zander.init import generate_template_structure
from zander.model.template import Template
from zander.provider.template import TemplateProvider
from zander.template_engine import TemplateEngine
from zander.utils import package_config_utils
from zander.utils import yaml_utils
from zander.utils.package_config_utils import get_install_dir


class InvalidDependencyError(Exception):
    def __str__(self):
        dependency, = self.args

        return "Invalid dependency {0}. " \
               "Expect it exists in <workspace>/code-gen-template-<name> or is a git url".format(dependency)


class DependencyInstaller(object):
    def __init__(self, path):
        self.path = path
        self.install_dir = get_install_dir(path)

    @property
    def workspace_dir(self):
        return abspath(join(self.path, pardir))

    def install(self):
        """
        Install dependencies

        :return:
        :rtype:
        """
        package_config = package_config_utils.load(self.path)
        # workspace_dir = abspath(join(self.path, pardir))
        # install_dir = abspath(join(self.path, '.code-gen'))

        if not exists(self.install_dir):
            makedirs(self.install_dir)

        # Create template folder
        generate_template_structure(self.path)

        for dependency in package_config.dependencies:
            print('Install dependency %s...' % dependency)

            if dependency.is_git:
                self._install_from_git(dependency)
            elif self._in_workspace(dependency):
                self._install_from_workspace(dependency)
            elif self._in_code_gen(dependency):
                print('Ignore')
            else:
                raise InvalidDependencyError(dependency)

            dependency_install_dir = join(self.install_dir, dependency.name)

            template = Template(dependency_install_dir)

            engine = TemplateEngine(template, project_dir=self.path)

            # Load _install() method of dependency if any
            if template.install:
                ret = template.install(engine.default_params)
                print(ret)

                self._build_data(dependency, ret)

    def _build_data(self, dependency, ret):
        data = ret.get('data')
        if data:
            dependency_data_file = join(self.path, 'template/data', dependency.name + '.yml')
            print(dependency_data_file)

            if not exists(dependency_data_file):
                yaml_utils.write(dependency_data_file, data)

    def _in_code_gen(self, dependency):
        return exists(join(self.install_dir, dependency.name))

    def _in_workspace(self, dependency):
        return exists(self._get_dependency_source(dependency))

    def _get_dependency_source(self, dependency):
        return join(self.workspace_dir, 'code-gen-template-%s' % dependency)

    def _install_from_workspace(self, dependency):
        dependency_install_dir = join(self.install_dir, dependency.name)
        # print(dependency_source, dependency_install_dir)

        if exists(dependency_install_dir):
            unlink(dependency_install_dir)

        symlink(self._get_dependency_source(dependency), dependency_install_dir)

    def _install_from_git(self, dependency):
        dep_dir = join(self.install_dir, dependency.name)
        if not exists(dep_dir):
            print('Clone %s' % dependency.origin)
            cmd = 'git clone {0} {1}'.format(dependency.origin, dependency.name)
            subprocess.call(shlex.split(cmd), cwd=self.install_dir)
        else:
            print('Update %s' % dependency.origin)
            cmd = 'git pull'
            subprocess.call(shlex.split(cmd), cwd=dep_dir)
