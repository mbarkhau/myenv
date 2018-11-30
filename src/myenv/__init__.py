# This file is part of the myenv project
# https://github.com/mbarkhau/myenv
#
# (C) 2018 Manuel Barkhau (@mbarkhau)
# SPDX-License-Identifier: MIT
"""Environment variable parsing using type annotations.

Usage:

>>> import os
>>> os.environ['CREDENTIALS_USER'] = "franz"
>>> os.environ['CREDENTIALS_KEY'] = "supersecret"
>>>
>>> class Credentials(BaseEnv):
...     _environ_prefix = "CREDENTIALS_"
...     user : str = "user"
...     key : str
...
>>> creds = Credentials()
>>> creds.user
'franz'
>>> creds.key
'supersecret'
>>> Credentials() is Credentials()  # singleton
True
"""

import os
import typing as typ
import pathlib as pl


__version__ = "v201809.0002-beta"


Environ = typ.MutableMapping[str, str]


EnvType = typ.TypeVar('EnvType', bound='BaseEnv')


def _iter_env_config(env_name: str) -> typ.Iterable[typ.Tuple[str, str]]:
    env_config_dir = os.getenv('ENV_CONFIG_DIR', ".")
    CONFIG_DIR     = pl.Path(env_config_dir) / "config"
    config_files   = [CONFIG_DIR / (env_name + ".env")]
    if env_name != 'prod':
        config_files.append(CONFIG_DIR / "prod.env")

    for config_file in config_files:
        if not config_file.exists():
            continue

        with config_file.open(mode="rt", encoding="utf-8") as fh:
            config_lines = fh.readlines()

        for line in config_lines:
            if "=" in line and not line.startswith("#"):
                name, value = line.strip().split("=", 1)
                yield name.strip(), value


_environ_initialized: typ.Set[int] = set()


def _init_environ(environ: Environ = None) -> None:
    if id(environ) in _environ_initialized:
        return

    if environ is None:
        environ = os.environ

    env_name = os.getenv('ENV', 'prod').lower()

    for name, value in _iter_env_config(env_name):
        if name not in environ:
            environ[name] = value.strip()

    _environ_initialized.add(id(environ))


__fallback_sentinel__ = '__fallback_sentinel__'


FieldType  = typ.Any
FieldValue = typ.Any


class _Field(typ.NamedTuple):

    fname   : str
    ftyp    : FieldType
    env_key : str
    fallback: FieldValue


def _iter_fields(env_type: typ.Type[EnvType]) -> typ.Iterable[_Field]:
    prefix = env_type._environ_prefix or ""
    for fname, ftyp in env_type.__annotations__.items():
        fallback = getattr(env_type, fname, __fallback_sentinel__)
        env_key  = (prefix + fname).upper()
        yield _Field(fname, ftyp, env_key, fallback)


def _parse_bool(val: str) -> bool:
    if val.lower() in ("1", "true"):
        return True
    elif val.lower() in ("0", "false"):
        return False
    else:
        raise ValueError(val)


def _parse_list_val(val: str, ftype: FieldType) -> typ.List[FieldValue]:
    list_strvals = [strval for strval in val.split(os.pathsep)]
    if ftype.__args__ == (str,):
        return list_strvals
    elif ftype.__args__ == (pl.Path,):
        return [pl.Path(listval) for listval in list_strvals]
    elif ftype.__args__ == (int,):
        return [int(listval, 10) for listval in list_strvals]
    elif ftype.__args__ == (float,):
        return [float(listval) for listval in list_strvals]
    elif ftype.__args__ == (bool,):
        return [_parse_bool(listval) for listval in list_strvals]
    else:
        raise TypeError(ftype)


def _parse_val(val: str, ftype: FieldType) -> FieldValue:
    if ftype == str:
        return val
    elif ftype == bool:
        return _parse_bool(val)
    elif ftype == int:
        return int(val, 10)
    elif ftype == float:
        return float(val)
    elif ftype == pl.Path:
        return pl.Path(val)
    elif ftype.__name__ == 'List':
        return _parse_list_val(val, ftype)
    elif ftype.__name__ == 'Set':
        return set(_parse_list_val(val, ftype))
    elif callable(ftype):
        return ftype(val)
    else:
        raise TypeError(ftype)


# Cache for already loaded environment configs. Environment
# variables are only parsed once during initialization.

EnvMapKey = typ.Tuple[typ.Type[EnvType], int]
EnvMap    = typ.Dict[EnvMapKey, EnvType]

_envmap: EnvMap = {}


class _Singleton(type):
    def __call__(cls, *args, **kwargs) -> EnvType:
        env_cls = typ.cast(typ.Type[EnvType], cls)
        environ: Environ = kwargs.get('environ', os.environ)
        envmap_key = (env_cls, id(environ))

        if envmap_key not in _envmap:
            _init_environ(environ)
            _envmap[envmap_key] = env_cls.__new__(env_cls, environ=environ)

        return _envmap[envmap_key]


class BaseEnv(metaclass=_Singleton):
    """The main Base class.

    Subclasses of BaseEnv are only instantiated once (singleton).
    """

    _environ_prefix: typ.Optional[str] = None

    def __new__(cls: typ.Type[EnvType], **kwargs) -> EnvType:
        """Create a new env instance.

        This should not be called from outside of myenv.
        """
        environ: Environ = kwargs['environ']
        typename = cls.__name__
        init_kwargs: typ.MutableMapping[str, typ.Any] = {}
        for field in _iter_fields(cls):
            if field.env_key in environ:
                try:
                    raw_env_val = environ[field.env_key]
                    init_kwargs[field.fname] = _parse_val(raw_env_val, field.ftyp)
                except ValueError as err:
                    raise ValueError(
                        f"Invalid value '{raw_env_val}' for {field.env_key}. "
                        f"Attepmted to parse '{typename}.{field.fname}' with '{field.ftyp}'.",
                        err,
                    )
            elif field.fallback != __fallback_sentinel__:
                init_kwargs[field.fname] = field.fallback
            else:
                raise KeyError(
                    f"No environment variable {field.env_key} "
                    + f"found for field {typename}.{field.fname}"
                )

        env = super(BaseEnv, cls).__new__(cls)
        env.__init__(**init_kwargs)
        return env

    def __init__(self, **kwargs) -> None:
        for key, val in kwargs.items():
            setattr(self, key, val)

    def _varnames(self) -> typ.List[str]:
        prefix = self._environ_prefix or ""
        return [
            (prefix + attrname).upper()
            for attrname in type(self).__annotations__
            if not attrname.startswith("_")
        ]

    def _asdict(self):
        pass


def parse(env_type: typ.Type[EnvType], environ: Environ = os.environ) -> EnvType:
    """Create an instance of an env.

    This is depricated, just instantiate like a normal class
    - myenv.parse(MyEnv)
    + MyEnv()
    """
    return env_type(environ=environ)
