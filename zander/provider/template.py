# encoding=utf-8
from os.path import join, exists

from zander.exception.package_config import InvalidCodeGenDependencyError
from zander.model.template import Template
from zander.utils import package_config_utils
from zander.utils.package_config_utils import get_install_dir


class TemplateProvider(object):
    def get(self, path):
        """
        Get template by loading `.code-gen.yml` file

        :param path:
        :type path:
        :return:
        :rtype:
        """
        package_config = package_config_utils.load(path)

        template = Template()
        install_dir = get_install_dir(project_dir=path)

        for dependency in package_config.dependencies:
            dependency_path = join(install_dir, dependency.name)
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

    def get_dependency(self, name):
        install_dir = get_install_dir(project_dir=None)

        dependency_path = join(install_dir, name)
        if not exists(dependency_path):
            raise InvalidCodeGenDependencyError(name, dependency_path)

        return Template(dependency_path)
