class PackageConfig(object):
    def __init__(self, data):
        self.data = data

    @property
    def dependencies(self):
        return self.data.get('dependencies', [])
