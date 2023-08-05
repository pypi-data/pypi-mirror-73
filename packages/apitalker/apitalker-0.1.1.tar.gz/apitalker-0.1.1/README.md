# Apitalker

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
    - [Examples](#examples)

## About <a name = "about"></a>

Python3 library. Wrapper for [Apitalks API](https://www.api.store/) calls. Enables simple call for api resource via `query` method with optional use of available parameters, as specified in [Apitalks documentation](https://www.api.store/czso.cz/dokumentace#section/Query-parametry).

## Getting Started <a name = "getting_started"></a>

These instructions will get you up and running.

### Prerequisites

What things you need to install the software.

    - Python 3+

### Installing

To install this package, simply use standard `pip install apitalker` or clone this repo and run `python setup.py install`.

## Usage <a name = "usage"></a>

apitalker is used as any other library.

```
from apitalker.api import API

api = API("yourAPIkeygoeshere")
data = api.query([resource], [...params])
```

### Examples <a name = "examples"></a>

**Call resource only, with no query parameters**

As is specified in [API documentation](https://www.api.store/czso.cz/dokumentace#section/Query-parametry), without any query parameters provided, API call will return one "page" of results, which equals of maximum of 30 data entries and 0 "pages" will be skipped.

```
from apitalker.api import API

api = API("yourAPIkeygoeshere")
data = api.query("/czso.cz/lide-domy-byty")
```

**Call resource with limited page size and skipped several pages**

```
from apitalker.api import API

api = API("yourAPIkeygoeshere")
data = api.query("/czso.cz/lide-domy-byty", limit=10, skip=10)
```

**Returned data can be ordered**

Pay attention to the quotes usage in the `order` parameter values!

```
from apitalker.api import API

api = API("yourAPIkeygoeshere")
data = api.query("/czso.cz/lide-domy-byty", limit=10, skip=10, order='"nazev ASC, u01 DESC"')
```

**Other filtering is possible using `where` parameter**

This is dependent on the data source.

```
from apitalker.api import API

api = API("yourAPIkeygoeshere")
data = api.query("/czso.cz/lide-domy-byty", where='"uzkod":568741, "year":1999')
```