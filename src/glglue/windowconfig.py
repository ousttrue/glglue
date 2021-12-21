from typing import NamedTuple


class WindowConfig(NamedTuple):
    x: int
    y: int
    width: int
    height: int
    is_maximized: bool
