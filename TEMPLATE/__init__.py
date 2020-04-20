import pkg_resources

# Import implementation modules
from .helloworld import hello

try:
    __version__ = pkg_resources.get_distribution("TEMPLATE").version
except Exception:  # pragma: nocover
    # Local copy, not installed with setuptools
    __version__ = "999"


__all__ = ("__version__", "hello")
