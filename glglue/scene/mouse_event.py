from typing import Optional, List, Callable, TypeAlias
from typing_extensions import Protocol
from glglue.frame_input import FrameInput


Callback: TypeAlias = Callable[[FrameInput, Optional[FrameInput]], None]
BeginEndCallback: TypeAlias = Callable[[FrameInput], None]
DragCallback: TypeAlias = Callable[[FrameInput, int, int], None]


class DragInterface(Protocol):
    def begin(self, mouse_input: FrameInput):
        ...

    def drag(self, mouse_input: FrameInput, dx: int, dy: int):
        ...

    def end(self, mouse_input: FrameInput):
        ...


class MouseEvent:
    def __init__(self) -> None:
        self.callbacks: List[Callback] = []
        self.last_input: Optional[FrameInput] = None

        # highlevel event
        self.left_active = None
        self.left_pressed: List[BeginEndCallback] = []
        self.left_drag: List[DragCallback] = []
        self.left_released: List[BeginEndCallback] = []
        self.right_active = None
        self.right_pressed: List[BeginEndCallback] = []
        self.right_drag: List[DragCallback] = []
        self.right_released: List[BeginEndCallback] = []
        self.middle_active = None
        self.middle_pressed: List[BeginEndCallback] = []
        self.middle_drag: List[DragCallback] = []
        self.middle_released: List[BeginEndCallback] = []

        self.wheel: List[Callable[[int], None]] = []
        self.nvg = None

    def __iadd__(self, callback: Callback):
        self.callbacks.append(callback)
        return self

    def process(self, current: FrameInput):
        for callback in self.callbacks:
            callback(current, self.last_input)

        #
        # highlevel event
        #
        dx = 0
        dy = 0
        if self.last_input:
            dx = current.mouse_x - self.last_input.mouse_x
            dy = current.mouse_y - self.last_input.mouse_y

        # pressed
        if (not self.last_input or not self.last_input.mouse_left) and current.mouse_left:
            self.left_active = (current.mouse_x, current.mouse_y)
            for callback in self.left_pressed:
                callback(current)
        if (
            not self.last_input or not self.last_input.mouse_right
        ) and current.mouse_right:
            self.right_active = (current.mouse_x, current.mouse_y)
            for callback in self.right_pressed:
                callback(current)
        if (
            not self.last_input or not self.last_input.mouse_middle
        ) and current.mouse_middle:
            self.middle_active = (current.mouse_x, current.mouse_y)
            for callback in self.middle_pressed:
                callback(current)

        # drag
        if current.mouse_left:
            # self.left_active = True
            for callback in self.left_drag:
                callback(current, dx, dy)
        if current.mouse_right:
            # self.right_active = True
            for callback in self.right_drag:
                callback(current, dx, dy)
        if current.mouse_middle:
            # self.middle_active = True
            for callback in self.middle_drag:
                callback(current, dx, dy)

        # released
        if self.left_active and not current.mouse_left:
            for callback in self.left_released:
                callback(current)
            self.left_active = None
        if self.right_active and not current.mouse_right:
            for callback in self.right_released:
                callback(current)
            self.right_active = None
        if self.middle_active and not current.mouse_middle:
            for callback in self.middle_released:
                callback(current)
            self.middle_active = None

        if current.mouse_wheel:
            for callback in self.wheel:
                callback(current.mouse_wheel)

        self.last_input = current

    def bind_left_drag(self, drag_handler: DragInterface):
        self.left_pressed.append(drag_handler.begin)
        self.left_drag.append(drag_handler.drag)
        self.left_released.append(drag_handler.end)

    def bind_right_drag(self, drag_handler: DragInterface):
        self.right_pressed.append(drag_handler.begin)
        self.right_drag.append(drag_handler.drag)
        self.right_released.append(drag_handler.end)

    def bind_middle_drag(self, drag_handler: DragInterface):
        self.middle_pressed.append(drag_handler.begin)
        self.middle_drag.append(drag_handler.drag)
        self.middle_released.append(drag_handler.end)
