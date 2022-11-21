import sys
from typing import Optional
import datetime
import os
import pathlib
import platform
import ctypes
from glglue.frame_input import FrameInput

if platform.system() == "Windows":
    if "PYSDL2_DLL_PATH" in os.environ:
        if os.path.exists(os.environ["PYSDL2_DLL_PATH"]):
            # OK
            pass
        else:
            del os.environ["PYSDL2_DLL_PATH"]

    if "PYSDL2_DLL_PATH" not in os.environ:
        try:
            import sdl2dll
        except ImportError:
            exe = pathlib.Path(sys.executable)
            sdl2dll = exe.parent / "sdl2.dll"
            if sdl2dll.exists():
                os.environ["PYSDL2_DLL_PATH"] = str(exe.parent)

from sdl2 import *


class LoopManager:
    def __init__(self, *, resizable=True, **kw):
        title = kw.get("title", b"glglue.pysdl2")

        # window state
        self.width = kw.get("width", 600)
        self.height = kw.get("height", 400)
        self.x = 0
        self.y = 0
        self.left_down = False
        self.right_down = False
        self.middle_down = False

        SDL_Init(SDL_INIT_VIDEO)
        SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1)
        self.window = SDL_CreateWindow(
            title,
            SDL_WINDOWPOS_UNDEFINED,
            SDL_WINDOWPOS_UNDEFINED,
            self.width,
            self.height,
            SDL_WINDOW_OPENGL,
        )
        SDL_GL_CreateContext(self.window)

        if resizable:
            SDL_SetWindowResizable(self.window, True)

        self.event = SDL_Event()

    def begin_frame(self) -> Optional[FrameInput]:
        """
        returns elapsed milliseconds
        """
        wheel = 0
        while SDL_PollEvent(ctypes.byref(self.event)) != 0:
            if self.event.type == SDL_QUIT:
                return
            elif self.event.type == SDL_KEYDOWN:
                # self.controller.onKeyDown(self.event.key.keysym.sym)
                pass
            elif self.event.type == SDL_MOUSEBUTTONDOWN:
                if self.event.button.button == SDL_BUTTON_LEFT:
                    self.left_down = True
                elif self.event.button.button == SDL_BUTTON_MIDDLE:
                    self.middle_down = True
                elif self.event.button.button == SDL_BUTTON_RIGHT:
                    self.right_down = True
            elif self.event.type == SDL_MOUSEBUTTONUP:
                if self.event.button.button == SDL_BUTTON_LEFT:
                    self.left_down = False
                elif self.event.button.button == SDL_BUTTON_MIDDLE:
                    self.middle_down = False
                elif self.event.button.button == SDL_BUTTON_RIGHT:
                    self.right_down = False
            elif self.event.type == SDL_MOUSEMOTION:
                self.x = self.event.motion.x
                self.y = self.event.motion.y
            elif self.event.type == SDL_MOUSEWHEEL:
                wheel = self.event.wheel.y
            elif self.event.type == SDL_WINDOWEVENT:
                if self.event.window.event == SDL_WINDOWEVENT_RESIZED:
                    self.width = self.event.window.data1
                    self.height = self.event.window.data2

        return FrameInput(
            elapsed_time=datetime.timedelta(microseconds=SDL_GetTicks()),
            mouse_x=self.x,
            mouse_y=self.y,
            width=self.width,
            height=self.height,
            mouse_left=self.left_down,
            mouse_middle=self.middle_down,
            mouse_right=self.right_down,
            mouse_wheel=wheel,
        )

    def end_frame(self):
        SDL_GL_SwapWindow(self.window)
