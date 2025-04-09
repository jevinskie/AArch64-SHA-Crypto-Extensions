import bidict


class UniqueBiDict(bidict.bidict):
    """bidict with additional requirement that keys must be disjoint from values"""

    def __getitem__(self, key):
        sentinel = object()
        a = self._fwdm.get(key, sentinel)
        b = self._invm.get(key, sentinel)
        if a is sentinel and b is sentinel:
            raise KeyError(key)
        if not ((a is sentinel) ^ (b is sentinel)):
            raise KeyError(key)
        return a if b is sentinel else b
