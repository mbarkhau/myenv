# MyENV: Environment Variable Parsing using Type annotation


[![Build Status][build_img]][build_ref]
[![Code Coverage][codecov_img]][codecov_ref]
[![MIT License][license_img]][license_ref]
[![Code Style: sjfmt][style_img]][style_ref]
[![Type Checked with mypy][mypy_img]][mypy_ref]
[![PyCalVer v201811.0001-alpha][version_img]][version_ref]
[![PyPI Version][pypi_img]][pypi_ref]
[![PyPI Downloads][downloads_img]][downloads_ref]
[![PyPI Wheel][wheel_img]][wheel_ref]
[![Supported Python Versions][pyversions_img]][pyversions_ref]


|            Name            |    role    |  since  | until |
|----------------------------|------------|---------|-------|
| Manuel Barkhau (@mbarkhau) | maintainer | 2018-09 | -     |


MyENV parses you're environment variables using type annotations
and defaults declared like this:

```python

import myenv
import dblib


class DBEnv(myenv.BaseEnv):

    _environ_prefix = "DATABASE_"

    vendor    : str  = "postgres"
    host      : str  = "127.0.0.1"
    port      : int  = 5432
    user      : str  = "myuser"
    password  : str
    name      : str  = "app_db_v1"
    read_only : bool = True

    @property
    def url(self):
        db = self
        return f"{db.vendor}://{db.user}:{db.password}@{db.host}:{db.port}/{db.name}"


# parses from os.environ
db = DBEnv()

conn = dblib.connect(db.url, read_only=dbenv.read_only)
```


[build_img]: https://gitlab.com/mbarkhau/myenv/badges/master/pipeline.svg
[build_ref]: https://gitlab.com/mbarkhau/myenv/pipelines

[codecov_img]: https://gitlab.com/mbarkhau/myenv/badges/master/coverage.svg
[codecov_ref]: https://mbarkhau.gitlab.io/myenv/cov

[license_img]: https://img.shields.io/badge/License-MIT-blue.svg
[license_ref]: https://gitlab.com/mbarkhau/myenv/blob/master/LICENSE

[mypy_img]: https://img.shields.io/badge/mypy-checked-green.svg
[mypy_ref]: http://mypy-lang.org/

[style_img]: https://img.shields.io/badge/code%20style-%20sjfmt-f71.svg
[style_ref]: https://gitlab.com/mbarkhau/straitjacket/

[pypi_img]: https://img.shields.io/pypi/v/myenv.svg
[pypi_ref]: https://gitlab.com/mbarkhau/myenv/blob/master/CHANGELOG.rst

[downloads_img]: https://pepy.tech/badge/myenv
[downloads_ref]: https://pepy.tech/project/myenv

[version_img]: https://img.shields.io/badge/PyCalVer-v201811.0002--alpha-blue.svg
[version_ref]: https://pypi.org/project/pycalver/

[wheel_img]: https://img.shields.io/pypi/wheel/myenv.svg
[wheel_ref]: https://pypi.org/project/myenv/#files

[pyversions_img]: https://img.shields.io/pypi/pyversions/myenv.svg
[pyversions_ref]: https://pypi.python.org/pypi/myenv
