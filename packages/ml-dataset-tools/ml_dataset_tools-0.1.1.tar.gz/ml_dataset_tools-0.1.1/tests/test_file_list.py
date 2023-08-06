import ml_dataset_tools as mdt
import numpy as np
import pytest


def test_empty_list():
    fl = mdt.FileList([])

    assert len(fl) == 0

    with pytest.raises(IndexError):
        fl[0]


def test_non_empty():
    fl = mdt.FileList(['aa', 'ab', 'bb'])

    assert len(fl) == 3
    assert fl[0] == 'aa'
    assert fl[1] == 'ab'
    assert fl[2] == 'bb'
    assert fl[-1] == 'bb'

    assert list(fl[:]) == ['aa', 'ab', 'bb']


def test_transform():
    fl = mdt.FileList(['aa', 'ab', 'bb'])

    res = fl.transform(lambda x: x.replace('a', 'c'))

    assert list(res) == ['cc', 'cb', 'bb']


def test_selector():
    fl = mdt.FileList(['aa', 'ab', 'bb'])

    res = fl.selector(lambda x: x.startswith('a'))

    assert list(res) == [True, True, False]
    assert isinstance(res, np.ndarray)
    assert res.dtype == np.bool


def test_side_effects():
    original_list = ['aa', 'ab', 'bb']
    fl = mdt.FileList(original_list)

    with pytest.raises(TypeError):  # cannot be changed
        fl[0] = 'XX'

    with pytest.raises(TypeError):  # cannot be changed
        fl[0:2] = ['XX', 'YY']

    fl.transform(lambda x: x.replace('a', 'c'))

    assert original_list == ['aa', 'ab', 'bb']
    assert list(fl) == ['aa', 'ab', 'bb']


def test_eq():
    fl1 = mdt.FileList(['aa', 'ab', 'bb'])

    assert fl1 == mdt.FileList(['aa', 'ab', 'bb'])
    assert fl1 != mdt.FileList(['aa'])
    assert fl1 != mdt.FileList(['aa', 'ab', 'Xb'])
    assert fl1 == fl1
    assert mdt.FileList([]) == mdt.FileList([])
