from __future__ import annotations

import importlib.metadata

import pytest
from packaging.version import parse as parse_version


def _import_or_skip(modname: str, minversion: str | None = None) -> tuple:
    """Build skip markers for an optional module

    :param str modname:
        Name of the optional module
    :param str minversion:
        Minimum required version
    :return:
        Tuple of

        has_module (bool)
            True if the module is available and >= minversion
        requires_module (decorator)
            Tests decorated with it will only run if the module is available
            and >= minversion
    """
    reason = "requires %s" % modname
    if minversion:
        reason += ">=%s" % minversion

    try:
        version = importlib.metadata.version(modname)
        has = True
    except importlib.metadata.PackageNotFoundError:
        has = False
    if has and minversion and parse_version(version) < parse_version(minversion):
        has = False

    func = pytest.mark.skipif(not has, reason=reason)
    return has, func


# TODO: optional dependencies here
has_numpy, requires_numpy = _import_or_skip("numpy")
