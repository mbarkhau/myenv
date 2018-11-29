import myenv
import pathlib as pl
import typing as typ


class DBEnv(myenv.BaseEnv):

    host     : str = "127.0.0.1"
    port     : int = 5432
    name     : str = "app_db_v1"
    user     : str = "app_user"
    password : str
    read_only: bool    = True
    ddl      : pl.Path = (pl.Path(".") / "create_tables.sql")


def test_parse():
    environ = {
        'MYAPP_DB_HOST'     : "1.2.3.4",
        'MYAPP_DB_PORT'     : "1234",
        'MYAPP_DB_NAME'     : "app_db_v2",
        'MYAPP_DB_USER'     : "new_user",
        'MYAPP_DB_PASSWORD' : "secret",
        'MYAPP_DB_READ_ONLY': "0",
        'MYAPP_DB_DDL'      : "~/mkdb.sql",
    }
    dbenv = myenv.parse(DBEnv, environ, prefix="MYAPP_DB_")

    assert dbenv.host     == "1.2.3.4"
    assert dbenv.port     == 1234
    assert dbenv.name     == "app_db_v2"
    assert dbenv.user     == "new_user"
    assert dbenv.password == "secret"
    assert dbenv.read_only is False
    assert isinstance(dbenv.ddl, pl.Path)
    assert str(dbenv.ddl).endswith("mkdb.sql")

    attrnames = [attrname for attrname in dir(dbenv) if not attrname.startswith("__")]
    assert len(attrnames) == 7


def test_defaults():
    dbenv = myenv.parse(DBEnv, environ={'PASSWORD': "secret"})
    assert dbenv.host     == "127.0.0.1"
    assert dbenv.port     == 5432
    assert dbenv.name     == "app_db_v1"
    assert dbenv.user     == "app_user"
    assert dbenv.password == "secret"
    assert dbenv.read_only is True

    assert isinstance(dbenv.ddl, pl.Path)
    assert str(dbenv.ddl).endswith("create_tables.sql")

    attrnames = [attrname for attrname in dir(dbenv) if not attrname.startswith("__")]
    assert len(attrnames) == 7


class TestEnv(myenv.BaseEnv):

    str_val_wo_default  : str
    str_val             : str = "foo"
    int_val_wo_default  : int
    int_val             : int = 123
    bool_val_wo_default : bool
    bool_val            : bool = True
    float_val_wo_default: float
    float_val           : float = 12.34
    path_val_wo_default : pl.Path
    path_val            : pl.Path = pl.Path("file.txt")
    paths_val_wo_default: typ.List[pl.Path]
    paths_val           : typ.List[pl.Path] = [
        pl.Path("file1.txt"),
        pl.Path("file2.txt"),
        pl.Path("file3.txt"),
    ]


def test_errors():
    try:
        dbenv = myenv.parse(TestEnv, {})
        assert False
    except KeyError as err:
        assert "STR_VAL_WO_DEFAULT" in str(err)

    try:
        dbenv = myenv.parse(TestEnv, {'STR_VAL_WO_DEFAULT': "bar"})
        assert False
    except KeyError as err:
        assert "INT_VAL_WO_DEFAULT" in str(err)

    good_environ = {
        'STR_VAL_WO_DEFAULT'  : "bar",
        'INT_VAL_WO_DEFAULT'  : "123",
        'BOOL_VAL_WO_DEFAULT' : "TRUE",
        'FLOAT_VAL_WO_DEFAULT': "123.456",
        'PATH_VAL_WO_DEFAULT' : "fileA.txt",
        'PATHS_VAL_WO_DEFAULT': "fileA.txt:fileB.txt:fileC.txt",
    }
    dbenv = myenv.parse(TestEnv, good_environ)

    try:
        bad_environ = good_environ.copy()
        bad_environ['INT_VAL'] = "abc"
        dbenv = myenv.parse(TestEnv, bad_environ)
        assert False
    except ValueError as err:
        assert 'INT_VAL' in str(err)
        assert 'abc' in str(err)
        assert 'TestEnv.int_val' in str(err)

    try:
        bad_environ = good_environ.copy()
        bad_environ['INT_VAL'] = "123af"
        dbenv = myenv.parse(TestEnv, bad_environ)
        assert False
    except ValueError as err:
        assert 'INT_VAL' in str(err)
        assert '123af' in str(err)
        assert 'TestEnv.int_val' in str(err)

    try:
        bad_environ = good_environ.copy()
        bad_environ['BOOL_VAL'] = "yes"
        dbenv = myenv.parse(TestEnv, bad_environ)
        assert False
    except ValueError as err:
        assert 'BOOL_VAL' in str(err)
        assert 'yes' in str(err)
        assert 'TestEnv.bool_val' in str(err)

    try:
        bad_environ = good_environ.copy()
        bad_environ['FLOAT_VAL'] = "abc.23"
        dbenv = myenv.parse(TestEnv, bad_environ)
        assert False
    except ValueError as err:
        assert 'FLOAT_VAL' in str(err)
        assert 'abc.23' in str(err)
        assert 'TestEnv.float_val' in str(err)


# def test_paths():
#     assert False
