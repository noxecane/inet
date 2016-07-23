from inet.utils import once

x = 2


def fn():
    global x
    x = x * 3
    return x


def test_once():
    f = once(fn)
    assert f() == 6
    assert f() == 6
