from typing import NamedTuple
import datetime


class FrameInput(NamedTuple):
    elapsed_milliseconds: datetime.timedelta = datetime.timedelta()
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    left_down: bool = False
    right_down: bool = False
    middle_down: bool = False
    wheel: int = 0
