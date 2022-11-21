from typing import NamedTuple, Callable, TypeAlias
import datetime


class FrameInput(NamedTuple):
    elapsed_time: datetime.timedelta = datetime.timedelta()
    width: int = 0
    height: int = 0
    mouse_x: int = 0
    mouse_y: int = 0
    mouse_left: bool = False
    mouse_right: bool = False
    mouse_middle: bool = False
    mouse_wheel: int = 0


RenderFunc: TypeAlias = Callable[[FrameInput], None]
