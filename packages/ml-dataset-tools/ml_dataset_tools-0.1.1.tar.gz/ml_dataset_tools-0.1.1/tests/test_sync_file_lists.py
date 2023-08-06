import ml_dataset_tools as mdt
import pytest


def test_simple():
    sl = mdt.SyncFileLists({'images': ['i1', 'i2'], 'classes': ['c1', 'c2']})

    assert list(sl['images']) == ['i1', 'i2']
    assert list(sl['classes']) == ['c1', 'c2']

    with pytest.raises(KeyError):
        sl['non-existent']


def test_with_selector():
    train = mdt.SyncFileLists.Type.train
    valid = mdt.SyncFileLists.Type.valid
    test = mdt.SyncFileLists.Type.test
    sl = mdt.SyncFileLists(
        dict_lists={'images': ['i1', 'i2', 'i3'], 'classes': ['c1', 'c2', 'c3']},
        selector=[train, test, train]
    )

    assert list(sl['images']) == ['i1', 'i2', 'i3']
    assert list(sl['images', train]) == ['i1', 'i3']
    assert list(sl['images', test]) == ['i2']
    assert list(sl['images', valid]) == []


def test_eq():
    train = mdt.SyncFileLists.Type.train
    valid = mdt.SyncFileLists.Type.valid
    test = mdt.SyncFileLists.Type.test
    sl = mdt.SyncFileLists(
        dict_lists={'images': ['i1', 'i2', 'i3'], 'classes': ['c1', 'c2', 'c3']},
        selector=[train, test, train]
    )

    assert sl == mdt.SyncFileLists(
        dict_lists={'images': ['i1', 'i2', 'i3'], 'classes': ['c1', 'c2', 'c3']},
        selector=[train, test, train]
    )
    assert sl != mdt.SyncFileLists(
        dict_lists={'images': ['i1', 'i2', 'i3']},
        selector=[train, test, train]
    )

    assert sl != mdt.SyncFileLists(
        dict_lists={'images': ['i1', 'i2', 'i3'], 'classes': ['c1', 'c2', 'c3']},
        selector=[test, test, train]
    )

    assert sl != mdt.SyncFileLists(
        dict_lists={'images': ['i1', 'i2', 'i3'], 'classes': ['c1', 'c2', 'c3']},
    )


def test_transform():
    train = mdt.SyncFileLists.Type.train
    valid = mdt.SyncFileLists.Type.valid
    test = mdt.SyncFileLists.Type.test
    sl = mdt.SyncFileLists(
        dict_lists={'images': ['i1', 'i2', 'i3'], 'classes': ['c1', 'c2', 'c3']},
        selector=[train, test, train]
    )

    result = sl.with_transformed('images', lambda x: x.replace('i', 'L'), 'labels')

    assert result == mdt.SyncFileLists(
        dict_lists={'images': ['i1', 'i2', 'i3'], 'classes': ['c1', 'c2', 'c3'], 'labels': ['L1', 'L2', 'L3']},
        selector=[train, test, train]
    )
    assert sl == mdt.SyncFileLists(
        dict_lists={'images': ['i1', 'i2', 'i3'], 'classes': ['c1', 'c2', 'c3']},
        selector=[train, test, train]
    )


def test_with_val():
    train = mdt.SyncFileLists.Type.train
    valid = mdt.SyncFileLists.Type.valid
    test = mdt.SyncFileLists.Type.test
    sl = mdt.SyncFileLists(
        dict_lists={'images': ['i1', 'i2', 'i3'], 'classes': ['c1', 'c2', 'c3']},
        selector=[train, test, train]
    )

    result = sl.with_val('images', lambda x: x[-1] in ['2', '3'])

    assert result == mdt.SyncFileLists(
        dict_lists={'images': ['i1', 'i2', 'i3'], 'classes': ['c1', 'c2', 'c3']},
        selector=[train, valid, valid]
    )
    assert sl == mdt.SyncFileLists(
        dict_lists={'images': ['i1', 'i2', 'i3'], 'classes': ['c1', 'c2', 'c3']},
        selector=[train, test, train]
    )


def test_filter_one_column():
    train = mdt.SyncFileLists.Type.train
    valid = mdt.SyncFileLists.Type.valid
    test = mdt.SyncFileLists.Type.test
    sl = mdt.SyncFileLists(
        dict_lists={'images': ['i1', 'i2', 'i3'], 'classes': ['c1', 'c2', 'c3']},
        selector=[train, test, train]
    )

    result = sl.filter(['images'], lambda x, *_: x[-1] in ['2', '3'])

    assert result == mdt.SyncFileLists(
        dict_lists={'images': ['i2', 'i3'], 'classes': ['c2', 'c3']},
        selector=[test, train]
    )
    assert sl == mdt.SyncFileLists(
        dict_lists={'images': ['i1', 'i2', 'i3'], 'classes': ['c1', 'c2', 'c3']},
        selector=[train, test, train]
    )


def test_filter_two_columns():
    train = mdt.SyncFileLists.Type.train
    valid = mdt.SyncFileLists.Type.valid
    test = mdt.SyncFileLists.Type.test
    sl = mdt.SyncFileLists(
        dict_lists={'images': ['X', 'Y', 'Y'], 'classes': ['good1', 'good2', 'bad3']},
        selector=[train, test, train]
    )

    result = sl.filter(['images', 'classes'], lambda i, c: i == 'Y' and c.startswith('good'))

    assert result == mdt.SyncFileLists(
        dict_lists={'images': ['Y'], 'classes': ['good2']},
        selector=[test]
    )

