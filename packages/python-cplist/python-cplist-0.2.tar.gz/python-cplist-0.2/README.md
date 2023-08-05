# CPList

A CPython parser/serializer for Apple's PropertyList format, using [libplist](https://github.com/libimobiledevice/libplist), with improved performance over Python's standard library `plistlib`.

[PyPi link](https://pypi.org/project/python-cplist/)

## Why?
This is around 3-4x faster than CPython's PList implementation.

`libplist` includes Cython bindings, but they are not compatible with `plistlib` since they load values as adapter types and not native Python types. (it's also slightly slower)


## Usage

```python

import cplist

obj = cplist.loads(data)
cplist.dumps(obj, fmt=cplist.FMT_XML)

obj = cplist.load(open('file'))
cplist.dumps(obj, open('file', 'wb'), fmt=cplist.FMT_BINARY)

```

## Installation

`pip install python-cplist`. 

Requires `libplist` to be installed (right now the path is hardcoded `/usr/local/lib`). 

On MacOS, run `brew install liplist`.

