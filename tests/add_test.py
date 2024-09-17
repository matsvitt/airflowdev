from airflowdev.my import add

def test_my():
    a = add(1,2)
    assert a == 3


def test_my2():
    a = add(1,2)
    assert a == 3.1
