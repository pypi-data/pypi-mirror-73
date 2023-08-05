#!/usr/bin/env python3
# Json library support hex escape.
import hexson


if __name__ == '__main__':
    data = {'a': '\u0000', 'b': [{"a": "\\x00", "b": -0.009}]}
    json = hexson.dumps(data)
    print(json)
    print(hexson.loads(json, utf_8_string=False))
