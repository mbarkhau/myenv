MyENV: Environment Variable Parsing with Types
==============================================

.. start-badges

.. list-table::
    :stub-columns: 1

    * - package
      - | |license| |wheel| |pyversions| |pypi| |version|
    * - tests
      - | |travis| |mypy| |coverage|

.. |travis| image:: https://api.travis-ci.org/mbarkhau/myenv.svg?branch=master
    :target: https://travis-ci.org/mbarkhau/myenv
    :alt: Build Status

.. |mypy| image:: http://www.mypy-lang.org/static/mypy_badge.svg
    :target: http://mypy-lang.org/
    :alt: Checked with mypy

.. |coverage| image:: https://codecov.io/gh/mbarkhau/myenv/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mbarkhau/myenv
    :alt: Code Coverage

.. |license| image:: https://img.shields.io/pypi/l/myenv.svg
    :target: https://github.com/mbarkhau/myenv/blob/master/LICENSE
    :alt: MIT License

.. |pypi| image:: https://img.shields.io/pypi/v/myenv.svg
    :target: https://github.com/mbarkhau/myenv/blob/master/CHANGELOG.rst
    :alt: PyPI Version

.. |version| image:: https://img.shields.io/badge/CalVer-v201809.0001--beta-blue.svg
    :target: https://calver.org/
    :alt: CalVer v201809.0002-beta

.. |wheel| image:: https://img.shields.io/pypi/wheel/myenv.svg
    :target: https://pypi.org/project/myenv/#files
    :alt: PyPI Wheel

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/myenv.svg
    :target: https://pypi.python.org/pypi/myenv
    :alt: Supported Python Versions


MyENV parses you're environment variables using types
and defaults declared like this:

.. code-block:: python

    import myenv
    import dblib

    class DBEnv(myenv.BaseEnv):

        host      : str  = "127.0.0.1"
        port      : int  = 5432
        name      : str  = "app_db_v1"
        user      : str  = "myuser"
        password  : str
        read_only : bool = True

    # parse from os.environ
    dbenv = myenv.parse(DBEnv)

    conn = dblib.connect(
        dbname=dbenv.name,
        user=dbenv.user,
        password=dbenv.password,
        port=dbenv.port,
        read_only=dbenv.read_only,
    )
