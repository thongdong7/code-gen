# encoding=utf-8
from os.path import join, exists

from code_gen.exception.package_config import InvalidCodeGenDependencyError
from code_gen.model.template import Template
from code_gen.utils import package_config_utils
from code_gen.utils.package_config_utils import get_install_dir


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
