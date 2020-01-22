import pkg_resources

# Import implementation modules
from .helloworld import hello

try:
    __version__ = pkg_resources.get_distribution("TEMPLATE").version
except Exception:
    # Local copy, not installed with setuptools
    __version__ = "unknown"


__all__ = ("__version__", "hello")
