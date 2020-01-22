import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("TEMPLATE").version
except Exception:
    # Local copy, not installed with setuptools
    __version__ = "unknown"

# Import implementation modules
from .helloworld import hello

__all__ = ("__version__", "hello")
