class ModulePath(object):
    '''
    This is an object that can represent its attribute tree
    as a path at any point in the attribute tree. The default
    delimeter for the path is '.'
    '''
    delimeter = '.'

    def __init__(self, path):
        self.path = path

    def __getattr__(self, path):
        return self.get_module('{}{}{}'.format(self.path, ModulePath.delimeter,  path))

    @classmethod
    def get_module(cls, name):
        return cls(name)
