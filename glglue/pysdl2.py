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


def mainloop(controller, title, width, height, **kw):
    SDL_Init(SDL_INIT_VIDEO)
    SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1)
    window = SDL_CreateWindow(title, SDL_WINDOWPOS_UNDEFINED,
                              SDL_WINDOWPOS_UNDEFINED, width, height, SDL_WINDOW_OPENGL)
    SDL_GL_CreateContext(window)
    controller.onResize(width, height)

    lastTime = SDL_GetTicks()
    event = SDL_Event()
    while True:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                return
            elif event.type == SDL_KEYDOWN:
                controller.onKeyDown(event.key.keysym.sym)
            elif event.type == SDL_MOUSEBUTTONDOWN:
                if event.button.button == SDL_BUTTON_LEFT:
                    controller.onLeftDown(event.button.x, event.button.y)
                elif event.button.button == SDL_BUTTON_MIDDLE:
                    controller.onMiddleDown(event.button.x, event.button.y)
                elif event.button.button == SDL_BUTTON_RIGHT:
                    controller.onRightDown(event.button.x, event.button.y)
            elif event.type == SDL_MOUSEBUTTONUP:
                if event.button.button == SDL_BUTTON_LEFT:
                    controller.onLeftUp(event.button.x, event.button.y)
                elif event.button.button == SDL_BUTTON_MIDDLE:
                    controller.onMiddleUp(event.button.x, event.button.y)
                elif event.button.button == SDL_BUTTON_RIGHT:
                    controller.onRightUp(event.button.x, event.button.y)
            elif event.type == SDL_MOUSEMOTION:
                controller.onMotion(event.motion.x, event.motion.y)
            elif event.type == SDL_MOUSEWHEEL:
                controller.onWheel(-event.wheel.y)

        time = SDL_GetTicks()
        d = time - lastTime
        lastTime = time
        if d > 0:
            controller.onUpdate(d)
            controller.draw()
            SDL_GL_SwapWindow(window)


if __name__ == "__main__":
    import glglue.sample
    mainloop(glglue.sample.SampleController(),
             title=b'pysdl2 sample', width=600, height=400)
