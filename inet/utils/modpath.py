class ModulePath(object):

    def __init__(self, path):
        self.path = path

    def __getattr__(self, path):
        return self.get_module('{}.{}'.format(self.path, path))

    @classmethod
    def get_module(cls, name):
        return cls(name)
