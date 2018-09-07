import myenv
import pathlib as pl
import typing as typ


class DBEnv(myenv.BaseEnv):

    host: str = "127.0.0.1"
    port: int = 5432
    name: str = "app_db_v1"
    user: str = "app_user"
    password: str
    read_only: bool = True
    ddl: pl.Path = (pl.Path(".") / "create_tables.sql")


def test_parse():
    environ = {
        "MYAPP_DB_HOST": "1.2.3.4",
        "MYAPP_DB_PORT": "1234",
        "MYAPP_DB_NAME": "app_db_v2",
        "MYAPP_DB_USER": "new_user",
        "MYAPP_DB_PASSWORD": "secret",
        "MYAPP_DB_READ_ONLY": "0",
        "MYAPP_DB_DDL": "~/mkdb.sql",
    }
    dbenv = myenv.parse(DBEnv, environ, prefix="MYAPP_DB_")

    assert dbenv.host == "1.2.3.4"
    assert dbenv.port == 1234
    assert dbenv.name == "app_db_v2"
    assert dbenv.user == "new_user"
    assert dbenv.password == "secret"
    assert dbenv.read_only is False
    assert isinstance(dbenv.ddl, pl.Path)
    assert str(dbenv.ddl).endswith("mkdb.sql")

    attrnames = [attrname for attrname in dir(dbenv) if not attrname.startswith("__")]
    assert len(attrnames) == 7


def test_defaults():
    dbenv = myenv.parse(DBEnv, environ={"PASSWORD": "secret"})
    assert dbenv.host == "127.0.0.1"
    assert dbenv.port == 5432
    assert dbenv.name == "app_db_v1"
    assert dbenv.user == "app_user"
    assert dbenv.password == "secret"
    assert dbenv.read_only is True

    assert isinstance(dbenv.ddl, pl.Path)
    assert str(dbenv.ddl).endswith("create_tables.sql")

    attrnames = [attrname for attrname in dir(dbenv) if not attrname.startswith("__")]
    assert len(attrnames) == 7
