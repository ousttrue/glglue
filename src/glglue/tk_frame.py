from typing import Callable
import sys
import logging
import dataclasses

import tkinter
from OpenGL import GL

# pip install pyopengltk
from pyopengltk import OpenGLFrame  # type: ignore

import glglue.scene
import glglue.scene.sample
import glglue.frame_input


LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class WindowStatus:
    on_updated: Callable[[], None]
    cursor_x: int = 0
    cursor_y: int = 0
    wheel: int = 0
    button_left: bool = False
    button_middle: bool = False
    button_right: bool = False

    def set_wheel(self, wheel: int) -> None:
        LOGGER.debug(f"{wheel}")
        self.wheel = wheel
        self.on_updated()

    def mouse_move(self, x: int, y: int) -> None:
        # only mouse pressed
        # LOGGER.debug(f"{x},{y}")
        self.cursor_x = x
        self.cursor_y = y
        self.on_updated()

    def mouse_left(self, x: int, y: int, press: bool) -> None:
        # LOGGER.debug(f"{x},{y},{press}")
        # self.cursor_x = x
        # self.cursor_y = y
        self.button_left = press
        if not press:
            self.on_updated()

    def mouse_middle(self, x: int, y: int, press: bool) -> None:
        # LOGGER.debug(f"{x},{y},{press}")
        # self.cursor_x = x
        # self.cursor_y = y
        self.button_middle = press
        if not press:
            self.on_updated()

    def mouse_right(self, x: int, y: int, press: bool) -> None:
        # LOGGER.debug(f"{x},{y},{press}")
        # self.cursor_x = x
        # self.cursor_y = y
        self.button_right = press
        if not press:
            self.on_updated()

    def make_frame(self, width: int, height: int) -> glglue.frame_input.FrameInput:
        wheel = self.wheel
        self.wheel = 0
        frame = glglue.frame_input.FrameInput(
            width=width,
            height=height,
            mouse_x=self.cursor_x,
            mouse_y=self.cursor_y,
            mouse_left=self.button_left,
            mouse_right=self.button_right,
            mouse_middle=self.button_middle,
            mouse_wheel=wheel,
            is_active=self.button_left or self.button_middle or self.button_right,
        )
        # LOGGER.debug(frame)
        return frame


class TkGlFrame(OpenGLFrame):
    def __init__(
        self,
        master,  # type: ignore
        on_render: Callable[[glglue.frame_input.FrameInput], None],
        *args,  # type: ignore
        **kw,  # type: ignore
    ):
        self.width = 0
        self.height = 0
        super(TkGlFrame, self).__init__(master, *args, **kw)  # type: ignore
        self.on_render = on_render
        self.status = WindowStatus(self.on_udpated)
        # self.bind("<Map>", self.onDraw)
        # self.bind("<Expose>", self.onDraw)
        # self.bind("<Configure>", self.onResize)
        self.bind(
            "<ButtonPress-1>",
            lambda e: self.status.mouse_left(e.x, e.y, True),
        )
        self.bind(
            "<ButtonRelease-1>",
            lambda e: self.status.mouse_left(e.x, e.y, False),
        )
        self.bind(
            "<B1-Motion>",
            lambda e: self.status.mouse_move(e.x, e.y),
        )
        self.bind(
            "<ButtonPress-2>",
            lambda e: self.status.mouse_middle(e.x, e.y, True),
        )
        self.bind(
            "<ButtonRelease-2>",
            lambda e: self.status.mouse_middle(e.x, e.y, False),
        )
        self.bind(
            "<B2-Motion>",
            lambda e: self.status.mouse_move(e.x, e.y),
        )
        self.bind(
            "<ButtonPress-3>",
            lambda e: self.status.mouse_right(e.x, e.y, True),
        )
        self.bind(
            "<ButtonRelease-3>",
            lambda e: self.status.mouse_right(e.x, e.y, False),
        )
        self.bind(
            "<B3-Motion>",
            lambda e: self.status.mouse_move(e.x, e.y),
        )

    def on_udpated(self):
        self.tkExpose(None)

    def initgl(self):
        """Initalize gl states when the frame is created"""
        # GL.glViewport(0, 0, self.width, self.height)
        # GL.glClearColor(0.0, 1.0, 0.0, 0.0)
        # self.start = time.time()
        # self.nframes = 0
        pass

    def redraw(self):
        """Render a single frame"""
        if self.width and self.height:
            self.on_render(self.status.make_frame(self.width, self.height))


def main():
    logging.basicConfig(
        format="[%(levelname)s] %(name)s.%(funcName)s: %(message)s", level=logging.DEBUG
    )

    class Frame(tkinter.Frame):
        def __init__(self, width, height, master=None, **kw):  # type: ignore
            super(Frame, self).__init__(master, **kw)  # type: ignore

            # setup opengl widget
            self.scene = glglue.scene.sample.SampleScene()
            self.glwidget = TkGlFrame(
                self, self.scene.render, width=width, height=height
            )
            self.glwidget.pack(fill=tkinter.BOTH, expand=True)
            # event binding(require focus)
            self.bind("<Key>", self.onKeyDown)  # type: ignore
            self.bind(
                "<MouseWheel>",
                lambda e: self.glwidget.status.set_wheel(-e.delta),
            )

        def onKeyDown(self, event) -> None:  # type: ignore
            key = event.keycode  # type: ignore
            if key == 27:
                # Escape
                sys.exit()
            if key == 81:
                # q
                sys.exit()
            else:
                LOGGER.debug(f"keycode: {key}")

    f = Frame(width=600, height=600)
    f.pack(fill=tkinter.BOTH, expand=True)
    f.focus_set()
    f.mainloop()


if __name__ == "__main__":
    main()
