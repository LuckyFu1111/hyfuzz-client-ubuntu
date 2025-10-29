"""Package version helper."""
from pathlib import Path

_VERSION_FILE = Path(__file__).resolve().parent.parent / "VERSION"
__all__ = ["__version__"]

try:
    __version__ = _VERSION_FILE.read_text(encoding="utf-8").strip()
except FileNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"
