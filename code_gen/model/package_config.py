import re

from functional import seq


class PackageConfig(object):
    def __init__(self, data):
        self.data = data

        self.dependencies = seq(self.data.get('dependencies', [])). \
            map(lambda d: Dependency(d)).list()


class Dependency(object):
    git_pattern = re.compile('^https://.*/([^/]+)\.git$')

    name_pattern = re.compile('^code-gen-template-(.*)$')

    def __init__(self, origin):
        self.origin = origin

        m = self.git_pattern.search(origin)
        if m:
            self.is_git = True
            self.long_name, self.name = self.parse_name(m.group(1))
        else:
            self.is_git = False
            self.long_name, self.name = self.parse_name(origin)

    @staticmethod
    def parse_name(text):
        m = Dependency.name_pattern.search(text)
        if m:
            return text, m.group(1)

        return text, text

    def __str__(self):
        return self.name

    __repr__ = __str__
