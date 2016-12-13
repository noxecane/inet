from inet.utils import decorators as decor

x = 2


def fn():
    global x
    x = x * 3
    return x


def test_once():
    f = decor.once(fn)
    assert f() == 6
    assert f() == 6
