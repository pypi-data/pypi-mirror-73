import numpy as np


class FileList:
    def __init__(self, lst):
        if isinstance(lst, FileList):
            lst = lst.lst[:]
        self.lst = np.array(lst)

    def selector(self, fn):
        cond = [fn(x) for x in self.lst]
        cond = np.array(cond, dtype='bool')
        return cond

    def transform(self, fn):
        return FileList([fn(x) for x in self.lst])

    def __len__(self):
        return len(self.lst)

    def __getitem__(self, idx):
        return self.lst[idx]

    def __eq__(self, other):
        if not isinstance(other, FileList):
            return False

        return np.array_equal(self.lst, other.lst)
