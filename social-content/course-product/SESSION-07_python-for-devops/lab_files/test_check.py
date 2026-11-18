from check import is_ok

def test_pass():
    assert is_ok(50, 90)

def test_fail():
    assert not is_ok(95, 90)
