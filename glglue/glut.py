#!/usr/bin/python
# coding: utf-8
""" [NAME] glglue.glut

[DESCRIPTION] use mainloop(Controller)
"""

from OpenGL.GLUT import *
import time
from logging import getLogger
import sys
import datetime
import glglue.frame_input

LOGGER = getLogger(__name__)


class GlutWindow:
    def __init__(
        self, width: int = 640, height: int = 480, title: bytes = b"glut sample"
    ) -> None:
        """[FUNCTIONS] setup and start glut mainloop"""
        self.mouse_left = False
        self.mouse_right = False
        self.mouse_middle = False
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.wheel = 0

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_STENCIL)  # type: ignore
        glutInitWindowSize(width, height)
        glutCreateWindow(title)
        # Windowのサイズが変わった時に呼ばれる関数を登録
        glutReshapeFunc(self.resize)
        # 描画時に呼ばれる関数を登録
        glutDisplayFunc(self.draw)
        # マウスボタン押し上げ時に呼ばれる関数
        glutMouseFunc(self.mouse)
        # マウスドラッグ時に呼ばれる関数
        glutMotionFunc(self.motion)
        glutPassiveMotionFunc(self.motion)
        # キーボードが押された時に呼ばれる関数
        glutKeyboardFunc(self.keyboard)

    def draw(self):
        pass

    def resize(self, w, h):
        self.width = w
        self.height = h

    def mouse(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                self.mouse_left = True
            else:
                self.mouse_left = False
        elif button == GLUT_MIDDLE_BUTTON:
            if state == GLUT_DOWN:
                self.mouse_middle = True
            else:
                self.mouse_middle = False
        elif button == GLUT_RIGHT_BUTTON:
            if state == GLUT_DOWN:
                self.mouse_right = True
            else:
                self.mouse_right = False
        elif button == 3:
            self.wheel = 1
        elif button == 4:
            self.wheel = -1
        else:
            LOGGER.warn("unknown mouse:", button, state, x, y)

        glutPostRedisplay()

    def motion(self, x, y):
        self.x = x
        self.y = y
        glutPostRedisplay()

    def keyboard(self, key, x, y):
        pass


class LoopManager:
    def __init__(self, **kw):
        self.w = GlutWindow(**kw)

    def begin_frame(self) -> glglue.frame_input.FrameInput:
        glutMainLoopEvent()
        clock = time.perf_counter()
        frame = glglue.frame_input.FrameInput(
            elapsed_time=datetime.timedelta(seconds=clock),
            mouse_x=self.w.x,
            mouse_y=self.w.y,
            width=self.w.width,
            height=self.w.height,
            mouse_left=self.w.mouse_left,
            mouse_middle=self.w.mouse_middle,
            mouse_right=self.w.mouse_right,
            mouse_wheel=self.w.wheel,
        )
        self.w.wheel = 0
        return frame

    def end_frame(self):
        glutSwapBuffers()
