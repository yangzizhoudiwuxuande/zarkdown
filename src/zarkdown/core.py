"""
向后兼容模块。
旧代码 `from zarkdown.core import zarkdown_to_html` 依然可用。
"""

from ._version import __version__
from .escape import escape_text, unescape_text
from .inline import parse_inline
from .validator import validate_zarkdown, print_errors
from .renderer import zarkdown_to_html
from .cli import main

__all__ = [
    "__version__",
    "escape_text",
    "unescape_text",
    "parse_inline",
    "validate_zarkdown",
    "print_errors",
    "zarkdown_to_html",
    "main",
]

if __name__ == "__main__":
    main()
