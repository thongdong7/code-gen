# encoding=utf-8
from os.path import join, exists

from code_gen.model.template import Template
from code_gen.utils import yaml_utils


class MissPackageFileError(Exception):
    def __str__(self):
        path, = self.args
        return 'Could not find file `.code-gen.yml` at {0}' \
            .format(path)


class PackageConfig(object):
    def __init__(self, data):
        self.data = data

    @property
    def dependencies(self):
        return self.data.get('dependencies', [])


class InvalidCodeGenDependencyError(Exception):
    def __str__(self):
        dependency, path = self.args
        return "Could not find dependency {0} at folder {1}".format(dependency, path)


class TemplateProvider(object):
    def get(self, path):
        """
        Get template by loading `.code-gen.yml` file

        :param path:
        :type path:
        :return:
        :rtype:
        """
        package_file = join(path, '.code-gen.yml')
        if not exists(package_file):
            raise MissPackageFileError(path)

        package_config_data = yaml_utils.load(package_file)
        package_config = PackageConfig(package_config_data)

        template = Template()
        for dependency in package_config.dependencies:
            dependency_path = join(path, '.code-gen', dependency)
            if not exists(dependency_path):
                raise InvalidCodeGenDependencyError(dependency, dependency_path)
            dependency_template = Template(dependency_path)

            template.merge(dependency_template)

        # Merge master template
        master_template_dir = join(path, 'template')
        if exists(master_template_dir):
            master_template = Template(master_template_dir)
            template.merge(master_template)

        return template
