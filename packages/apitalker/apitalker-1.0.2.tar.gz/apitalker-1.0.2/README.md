# Apitalker

![Upload Python Package](https://github.com/bednaJedna/att/workflows/Upload%20Python%20Package/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/att/badge/?version=latest)](https://att.readthedocs.io/en/latest/?badge=latest)

## Table of Contents

- [About](#about)
- [Documentation](#documentation)
- [Getting Started](#getting_started)
- [Usage](#usage)
  - [Examples](#examples)

## About <a name = "about"></a>

Python3 library. Wrapper for [Apitalks API](https://www.api.store/) calls. Enables simple calls for api resources with optional use of available parameters, as specified in [Apitalks documentation](https://www.api.store/czso.cz/dokumentace#section/Query-parametry).

Returned data (when method `apitalker.api.API.get_data()` is used) are handled by `apitalker.data.Data` class, which provides some convenient methods for working with data.

## Documentation <a name= "documentation"></a>

Documentation including examples is [HERE](https://att.readthedocs.io/en/latest/).

## Getting Started <a name = "getting_started"></a>

These instructions will get you up and running.

### Prerequisites

What things you need to install the software.

    - Python 3+

    - requests

    - pandas

### Installing

To install this package, simply use standard `pip install apitalker` or clone this repo and run `python setup.py install`.

## Usage <a name = "usage"></a>

See examples in [Documentation](https://att.readthedocs.io/en/latest/)