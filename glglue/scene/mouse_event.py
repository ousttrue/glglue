from typing import Optional, List, Callable, TypeAlias
from typing_extensions import Protocol
import abc
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
            dx = current.x - self.last_input.x
            dy = current.y - self.last_input.y

        # pressed
        if (not self.last_input or not self.last_input.left_down) and current.left_down:
            self.left_active = (current.x, current.y)
            for callback in self.left_pressed:
                callback(current)
        if (
            not self.last_input or not self.last_input.right_down
        ) and current.right_down:
            self.right_active = (current.x, current.y)
            for callback in self.right_pressed:
                callback(current)
        if (
            not self.last_input or not self.last_input.middle_down
        ) and current.middle_down:
            self.middle_active = (current.x, current.y)
            for callback in self.middle_pressed:
                callback(current)

        # drag
        if current.left_down:
            # self.left_active = True
            for callback in self.left_drag:
                callback(current, dx, dy)
        if current.right_down:
            # self.right_active = True
            for callback in self.right_drag:
                callback(current, dx, dy)
        if current.middle_down:
            # self.middle_active = True
            for callback in self.middle_drag:
                callback(current, dx, dy)

        # released
        if self.left_active and not current.left_down:
            for callback in self.left_released:
                callback(current)
            self.left_active = None
        if self.right_active and not current.right_down:
            for callback in self.right_released:
                callback(current)
            self.right_active = None
        if self.middle_active and not current.middle_down:
            for callback in self.middle_released:
                callback(current)
            self.middle_active = None

        if current.wheel:
            for callback in self.wheel:
                callback(current.wheel)

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

    def debug_draw(self):
        mouse_input = self.last_input
        if not mouse_input:
            return
        if not self.nvg:
            from pydear.utils.nanovg_renderer import NanoVgRenderer

            self.nvg = NanoVgRenderer()

        def draw_line(vg, sx, sy, ex, ey, r, g, b):
            nanovg.nvgSave(vg)
            nanovg.nvgStrokeWidth(vg, 1.0)
            nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(r, g, b, 255))
            nanovg.nvgFillColor(vg, nanovg.nvgRGBA(r, g, b, 255))

            nanovg.nvgBeginPath(vg)
            nanovg.nvgMoveTo(vg, sx, sy)
            nanovg.nvgLineTo(vg, ex, ey)
            nanovg.nvgStroke(vg)

            nanovg.nvgBeginPath(vg)
            nanovg.nvgCircle(vg, sx, sy, 4)
            nanovg.nvgFill(vg)

            nanovg.nvgBeginPath(vg)
            nanovg.nvgCircle(vg, ex, ey, 4)
            nanovg.nvgFill(vg)

            nanovg.nvgRestore(vg)

        with self.nvg.render(mouse_input.width, mouse_input.height) as vg:
            from pydear import nanovg

            match self.left_active:
                case (x, y):
                    draw_line(vg, x, y, mouse_input.x, mouse_input.y, 255, 0, 0)
            match self.middle_active:
                case (x, y):
                    draw_line(vg, x, y, mouse_input.x, mouse_input.y, 0, 255, 0)
            match self.right_active:
                case (x, y):
                    draw_line(vg, x, y, mouse_input.x, mouse_input.y, 0, 0, 255)
