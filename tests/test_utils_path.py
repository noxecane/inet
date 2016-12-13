from inet.utils.path import Path, Root


class NamePath(Path):

    def __call__(self):
        return self.root.student_name


class NameRoot(Root):

    path_cls = NamePath

    def __init__(self, name, student_name):
        super().__init__(name)
        self.student_name = student_name


def test_root_path():
    namepack = NameRoot('admin', 'Arewa')
    assert namepack.goods.get.path == 'admin.goods.get'
    assert namepack.goods.getID() == 'Arewa'
