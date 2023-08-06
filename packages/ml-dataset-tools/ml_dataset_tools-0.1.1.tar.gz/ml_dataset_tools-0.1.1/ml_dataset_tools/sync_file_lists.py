from enum import Enum

import numpy as np

from ml_dataset_tools.file_list import FileList


class SyncFileLists:
    class Type(Enum):
        train = 0,
        valid = 1,
        test = 2

    def __init__(self, dict_lists, selector=None):
        lens = [len(v) for k, v in dict_lists.items()]
        self.len_list = lens[0]
        assert all(l == self.len_list for l in lens)
        self.dict_lists = {k: FileList(v) for k, v in dict_lists.items()}
        if selector is None:
            selector = [self.Type.train for _ in range(self.len_list)]
        self._selector = np.array(selector)

    def __getitem__(self, key):
        if isinstance(key, str):
            name = key
            return self.dict_lists[name]

        name, ds_type = key
        assert isinstance(ds_type, self.Type)
        flag = [x == ds_type for x in self._selector]
        return self.dict_lists[name][flag]

    def __setitem__(self, name, file_list):
        if name in self.dict_lists:
            raise ValueError("key exists {}".format(name))

        if len(file_list) != self.len_list:
            raise ValueError("Wrong len {}. expected {}".format(len(file_list), self.len_list))

        self.dict_lists[name] = FileList(file_list)

    def __iter__(self):
        return iter(self.dict_lists.values())

    def with_transformed(self, name_src, tfm, name_dst):
        return SyncFileLists(
            dict_lists={
                name_dst: self[name_src].transform(tfm),
                **self.dict_lists
            },
            selector=self._selector
        )

    def with_val(self, name_src, fn):
        selector = [
            self.Type.valid if x else self.Type.train
            for x in self[name_src].selector(fn)
        ]
        return SyncFileLists(self.dict_lists, selector=selector)

    def filter(self, names, fn):
        selected_lists = [self.dict_lists[name] for name in names]
        flag = np.array([fn(*items) for items in zip(*selected_lists)], dtype='bool')
        return SyncFileLists(
            {name: lst[flag] for name, lst in self.dict_lists.items()},
            self._selector[flag]
        )

    @property
    def is_val(self):
        raise NotImplementedError("Use with_val insread")

    def __eq__(self, other):
        if type(other) != SyncFileLists:
            raise ValueError("Cannot compare {} to {}".format(type(self), type(other)))

        return self.dict_lists == other.dict_lists and np.array_equal(self._selector, other._selector)
