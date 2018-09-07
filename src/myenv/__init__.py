# This file is part of the myenv project
# https://github.com/mbarkhau/myenv
#
# (C) 2018 Manuel Barkhau (@mbarkhau)
# SPDX-License-Identifier: MIT

import os
import typing as typ
import pathlib as pl


class BaseEnv:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


__default_sentinel__ = '__default_sentinel__'


Environ = typ.Mapping[str, str]

EnvType = typ.TypeVar('EnvType', bound=BaseEnv)


def iter_fields(
    env_type: typ.Type[EnvType], prefix: str
) -> typ.Iterable[typ.Tuple[str, str, typ.Any, typ.Any]]:
    for field_name, field_type in env_type.__annotations__.items():
        default = getattr(env_type, field_name, __default_sentinel__)
        env_key = (prefix + field_name).upper()
        yield field_name, env_key, field_type, default


def parse_val(val: str, ftype: typ.Any) -> typ.Any:
    if ftype == str:
        return val
    elif ftype == bool:
        if val.lower() in ("1", "true"):
            return True
        elif val.lower() in ("0", "false"):
            return False
        else:
            raise ValueError(val)
    elif ftype == int:
        return int(val, 10)
    elif ftype == float:
        return float(val)
    elif ftype == pl.Path:
        return pl.Path(val)
    elif ftype._name == 'List':
        if ftype.__args__ == (pl.Path,):
            return [pl.Path(pathstr) for pathstr in val.split(os.pathsep)]
        elif ftype.__args__ == (str,):
            return [pathstr for pathstr in val.split(os.pathsep)]
    elif callable(ftype):
        return ftype(val)
    else:
        raise TypeError(ftype)


def parse(
    env_type: typ.Type[EnvType], environ: Environ = os.environ, prefix: str = None
) -> EnvType:
    if prefix is None:
        prefix = ""

    kwargs: typ.MutableMapping[str, typ.Any] = {}
    for fname, env_key, ftype, default in iter_fields(env_type, prefix):
        if env_key in environ:
            try:
                raw_env_val = environ[env_key]
                kwargs[fname] = parse_val(raw_env_val, ftype)
            except ValueError as err:
                raise ValueError(
                    f"Invalid value '{raw_env_val}' for {env_key}."
                    f"attepmted to parse with '{ftype}'."
                )
        elif default != __default_sentinel__:
            kwargs[fname] = default
        else:
            raise KeyError(
                f"No environment variable {env_key} found for field {env_type.__name__}.{fname}"
            )
    return env_type(**kwargs)
