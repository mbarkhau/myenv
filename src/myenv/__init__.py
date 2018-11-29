# This file is part of the myenv project
# https://github.com/mbarkhau/myenv
#
# (C) 2018 Manuel Barkhau (@mbarkhau)
# SPDX-License-Identifier: MIT

import os
import typing as typ
import pathlib as pl


__version__ = "v201809.0002-beta"


class BaseEnv:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def _asdict(self):
        pass


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
    elif ftype._name in ('List', 'Set'):
        list_strvals = [strval for strval in val.split(os.pathsep)]
        if ftype.__args__ == (str,):
            list_val = list_strvals
        elif ftype.__args__ == (pl.Path,):
            list_val = [pl.Path(listval) for listval in list_strvals]
        elif ftype.__args__ == (int,):
            list_val = [int(listval, 10) for listval in list_strvals]
        elif ftype.__args__ == (float,):
            list_val = [float(listval) for listval in list_strvals]
        elif ftype.__args__ == (bool,):
            list_val = []
            for listval in list_strvals:
                if listval.lower() in ("1", "true"):
                    list_val.append(True)
                elif listval.lower() in ("0", "false"):
                    list_val.append(False)
                else:
                    raise ValueError(listval)
        else:
            raise TypeError(ftype)

        if ftype._name == 'List':
            return list_val
        elif ftype._name == 'Set':
            return set(list_val)
        else:
            # This cannot happen
            raise TypeError(ftype)
    elif callable(ftype):
        return ftype(val)
    else:
        raise TypeError(ftype)


def parse(
    env_type: typ.Type[EnvType], environ: Environ = os.environ, prefix: str = None
) -> EnvType:
    if prefix is None:
        prefix = getattr(env_type, '_environ_prefix', "")

    typename = env_type.__name__
    kwargs: typ.MutableMapping[str, typ.Any] = {}
    for fname, env_key, ftype, default in iter_fields(env_type, prefix):
        if env_key in environ:
            try:
                raw_env_val = environ[env_key]
                kwargs[fname] = parse_val(raw_env_val, ftype)
            except ValueError as err:
                raise ValueError(
                    f"Invalid value '{raw_env_val}' for {env_key}. "
                    f"Attepmted to parse '{typename}.{fname}' with '{ftype}'."
                )
        elif default != __default_sentinel__:
            kwargs[fname] = default
        else:
            raise KeyError(f"No environment variable {env_key} found for field {typename}.{fname}")
    return env_type(**kwargs)
