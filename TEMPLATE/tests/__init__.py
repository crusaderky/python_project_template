from __future__ import annotations

import importlib.metadata

import pytest
from packaging import version


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
    reason = f"requires {modname}"
    if minversion:
        reason += f">={minversion}"

    has = True
    try:
        pkg_version = importlib.metadata.version(modname)
        if minversion and version.parse(pkg_version) < version.parse(
            minversion
        ):  # pragma: nocover
            has = False  # pragma: nocover
    except importlib.metadata.PackageNotFoundError:
        has = False

    func = pytest.mark.skipif(not has, reason=reason)
    return has, func


# TODO: optional dependencies here
has_numpy, requires_numpy = _import_or_skip("numpy")
has_numpy122, requires_numpy122 = _import_or_skip("numpy", "1.22")
