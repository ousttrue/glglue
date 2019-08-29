import sys
sys.path.append('.')
sys.path.append('..')

import os
import pathlib

if 'PYSDL2_DLL_PATH' not in os.environ:
    exe = pathlib.Path(sys.executable)
    sdl2dll = exe.parent / 'sdl2.dll'
    if sdl2dll.exists():
        os.environ['PYSDL2_DLL_PATH'] = str(exe.parent)

from sdl2 import *
import ctypes


class LoopManager:
    def __init__(self, controller, **kw):
        self.controller = controller
        title = kw.get('title', b'glglue.pysdl2')
        width = kw.get('width', 600)
        height = kw.get('height', 400)
        SDL_Init(SDL_INIT_VIDEO)
        SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1)
        self.window = SDL_CreateWindow(title, SDL_WINDOWPOS_UNDEFINED,
                                       SDL_WINDOWPOS_UNDEFINED, width, height,
                                       SDL_WINDOW_OPENGL)
        SDL_GL_CreateContext(self.window)
        self.controller.onResize(width, height)
        self.event = SDL_Event()

    def begin_frame(self):
        while SDL_PollEvent(ctypes.byref(self.event)) != 0:
            if self.event.type == SDL_QUIT:
                return
            elif self.event.type == SDL_KEYDOWN:
                self.controller.onKeyDown(self.event.key.keysym.sym)
            elif self.event.type == SDL_MOUSEBUTTONDOWN:
                if self.event.button.button == SDL_BUTTON_LEFT:
                    self.controller.onLeftDown(self.event.button.x,
                                               self.event.button.y)
                elif self.event.button.button == SDL_BUTTON_MIDDLE:
                    self.controller.onMiddleDown(self.event.button.x,
                                                 self.event.button.y)
                elif self.event.button.button == SDL_BUTTON_RIGHT:
                    self.controller.onRightDown(self.event.button.x,
                                                self.event.button.y)
            elif self.event.type == SDL_MOUSEBUTTONUP:
                if self.event.button.button == SDL_BUTTON_LEFT:
                    self.controller.onLeftUp(self.event.button.x,
                                             self.event.button.y)
                elif self.event.button.button == SDL_BUTTON_MIDDLE:
                    self.controller.onMiddleUp(self.event.button.x,
                                               self.event.button.y)
                elif self.event.button.button == SDL_BUTTON_RIGHT:
                    self.controller.onRightUp(self.event.button.x,
                                              self.event.button.y)
            elif self.event.type == SDL_MOUSEMOTION:
                self.controller.onMotion(self.event.motion.x,
                                         self.event.motion.y)
            elif self.event.type == SDL_MOUSEWHEEL:
                self.controller.onWheel(-self.event.wheel.y)

        return SDL_GetTicks()

    def end_frame(self):
        SDL_GL_SwapWindow(self.window)


if __name__ == "__main__":
    import glglue.sample
    controller = glglue.sample.SampleController()
    loop = LoopManager(controller)
    lastTime = 0
    while True:
        time = loop.begin_frame()
        if not time:
            break
        if lastTime == 0:
            lastTime = time
            continue
        d = time - lastTime
        lastTime = time
        if d:
            controller.onUpdate(d)
            controller.draw()
            loop.end_frame()
