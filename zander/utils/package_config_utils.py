from os.path import join, exists, expanduser, abspath

from zander.exception.package_config import MissPackageFileError
from zander.model.package_config import PackageConfig
from zander.utils import yaml_utils


def load(path):
    package_file = join(path, '.code-gen.yml')
    if not exists(package_file):
        raise MissPackageFileError(path)

    package_config_data = yaml_utils.load(package_file)
    return PackageConfig(package_config_data)


home_dir = expanduser("~")


def get_install_dir(project_dir):
    return abspath(join(home_dir, '.code-gen'))
