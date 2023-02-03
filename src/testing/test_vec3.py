
from src.algorithm_modules.data_structure.vector3 import Vector3

def test__vec_dot():
    a = Vector3(1,2,3)
    b = Vector3(4,5,6)
    c = Vector3(1,1,1)
    d = Vector3(0,0,0)
    e = Vector3(-5,-4,-3)
    f = Vector3(-3,2,-1)
    assert a.dot(b) == (1*4) + (2*5) + (3*6) == b.dot(a)
    assert a.dot(c) == 1+2+3 == c.dot(a)
    assert a.dot(d) == 0 == d.dot(a)
    assert b.dot(d) == 0 == d.dot(b)
    assert c.dot(d) == 0 == d.dot(c)
    assert b.dot(c) == 4+5+6 == c.dot(b)
    assert a.dot(e) == (-5)*1 + (-4)*2 + (-3)*3 == e.dot(a)
    assert a.dot(f) == -2 == f.dot(a)

# def test__