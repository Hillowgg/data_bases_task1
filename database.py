import re

_types = {
    '0': int,
    '1': float,
    '2': str,
    '3': bool,
    int: '0',
    float: '1',
    str: '2',
    bool: '3'
}

ValueType = int | float | str | bool


def _checkKey(key):
    if not isinstance(key, str):
        raise TypeError("Key must be str")
    if 1 < len(key) > 100:
        raise ValueError("Key length must be more than 0 and less than 101")


def _checkValueType(value):
    if type(value) not in _types:
        raise TypeError("Unsupported type of value")


class Row:
    def __init__(self, key: str = None, value: ValueType = None, raw=None):
        if raw:
            self._parseRaw(raw)
        else:
            _checkKey(key)
            _checkValueType(value)

            self._key = key
            self._value = value

    def setValue(self, value: ValueType):
        _checkValueType(value)
        self._value = value

    def getValue(self):
        return self._value

    def setKey(self, key: str):
        _checkKey(key)
        self._key = key

    def getKey(self):
        return self._key

    def _parseRaw(self, raw: str):
        key_len = int(raw[:2])
        type_ = _types[raw[2]]

        self._key = raw[3:3 + key_len]
        self._value = type_(raw[3 + key_len:-1])

    def __str__(self):
        if not self._key:
            raise RuntimeError("Set key before")
        if self._value is None:
            raise RuntimeError("Set value before")

        len_ = len(self._key)
        type_ = _types[type(self._value)]

        raw = f'{len_:02}{type_}{self._key}{self._value}'
        return raw


class DataBase:
    def __init__(self, path: str = None):
        self.path = path
        self._rows = []

    def connect(self):
        with open(self.path, 'r+') as f:
            for row in f.readlines():
                self._rows += [Row(raw=row)]

    def _findByKey(self, key: str) -> int:
        for i, row in enumerate(self._rows):
            if row.getKey() == key:
                return i
        return -1

    def get(self, key: str) -> Row | None:
        _checkKey(key)
        ind = self._findByKey(key)
        return self._rows[ind].getValue() if ind != -1 else None

    def set(self, key: str, *value: ValueType):
        value = ' '.join(value)
        _checkValueType(value)
        _checkKey(key)

        ind = self._findByKey(key)
        row = Row(key=key, value=value)

        if ind != -1:
            self._rows[ind] = row
            return 2
        else:
            self._rows.append(row)
            return 1

    def delete(self, key: str):
        _checkKey(key)
        ind = self._findByKey(key)

        if ind == -1:
            raise IndexError("Can't delete nothing")

        del self._rows[ind]
        return 1

    def keys(self, pattern: str):

        res = []

        try:
            for row in self._rows:
                if re.match(pattern, row.getKey()):
                    res.append(row.getKey())
        except re.error:
            return "Wrong regex"

        return res

    def exit(self):
        with open(self.path, 'w') as f:
            f.writelines([
                str(row) + '\n' for row in self._rows
            ])

        return 'exiting...'
