from os.path import join, exists

from code_gen.exception.package_config import MissPackageFileError
from code_gen.model.package_config import PackageConfig
from code_gen.utils import yaml_utils


def load(path):
    package_file = join(path, '.code-gen.yml')
    if not exists(package_file):
        raise MissPackageFileError(path)

    package_config_data = yaml_utils.load(package_file)
    return PackageConfig(package_config_data)
