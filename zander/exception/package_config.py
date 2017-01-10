class MissPackageFileError(Exception):
    def __str__(self):
        path, = self.args
        return 'Could not find file `.code-gen.yml` at {0}' \
            .format(path)


class InvalidCodeGenDependencyError(Exception):
    def __str__(self):
        dependency, path = self.args
        return "Could not find dependency {0} at folder {1}".format(dependency, path)
