class Path(object):
    '''
    This is an object that can represent its attribute tree
    as a path at any point in the attribute tree with delimeter
    for the path as '.'
    '''

    def __init__(self, root, path):
        '''
        Creates a new node in the path.
        @sig Path :: Root -> Str -> Path
        '''
        self.root = root
        self.path = path

    def __getattr__(self, path):
        return self.get_module(self.root, '%s.%s' % (self.path,  path))

    @classmethod
    def get_module(cls, root, name):
        '''
        Factory method for creating new nodes
        @sig get_module :: Root -> Str -> Path
        '''
        return cls(root, name)


class Root(object):
    '''
    This is an object that represent the root of any path attached
    to it. It is meant to store information for all the possible nodes
    to be created.
    '''

    '''
    Class that will be used to create child nodes
    '''
    path_cls = Path

    def __init__(self, name):
        '''
        Creates a root node for string tree.
        @sig Root :: Str ->  Root
        '''
        self.name = name

    def __getattr__(self, path):
        return self.path_cls(self, '%s.%s' % (self.name, path))
