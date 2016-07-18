class Path(object):
    '''
    This is an object that can represent its attribute tree
    as a path at any point in the attribute tree with delimeter
    for the path as '.'
    '''

    def __init__(self, path):
        self.path = path

    def __getattr__(self, path):
        return self.get_module('{}.{}'.format(self.path,  path))

    @classmethod
    def get_module(cls, name):
        return cls(name)
