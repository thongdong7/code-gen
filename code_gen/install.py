from os import makedirs, symlink, unlink

from code_gen.exception.package_config import InvalidCodeGenDependencyError
from code_gen.utils import package_config_utils
from os.path import join, exists, pardir, abspath


class DependencyInstaller(object):
    def __init__(self, path):
        self.path = path

    def install(self):
        """
        Install dependencies

        :return:
        :rtype:
        """
        package_config = package_config_utils.load(self.path)
        workspace_dir = abspath(join(self.path, pardir))
        install_dir = abspath(join(self.path, '.code-gen'))

        if not exists(install_dir):
            makedirs(install_dir)

        for dependency in package_config.dependencies:
            print('Install dependency %s...' % dependency)

            dependency_source = join(workspace_dir, 'code-gen-template-%s' % dependency)
            if not exists(dependency_source):
                raise InvalidCodeGenDependencyError(dependency, dependency_source)

            dependency_install_dir = join(install_dir, dependency)
            # print(dependency_source, dependency_install_dir)

            if exists(dependency_install_dir):
                unlink(dependency_install_dir)
            symlink(dependency_source, dependency_install_dir)
