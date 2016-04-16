#!/usr/bin/python
# coding: utf-8
""" [NAME] glglue.glut

[DESCRIPTION] use mainloop(Controller)
"""

from OpenGL.GLUT import *
import time
from logging import getLogger
logger = getLogger(__name__)


FPS=30
MSPF=int(1000.0/FPS)

_g_controller=None


def _resize(w, h):
    _g_controller.onResize(w, h)


def _mouse(button, state, x, y):
    if button==GLUT_LEFT_BUTTON:
        if state==GLUT_DOWN:
            if _g_controller.onLeftDown(x, y):
                glutPostRedisplay()
        else:
            if _g_controller.onLeftUp(x, y):
                glutPostRedisplay()
    elif button==GLUT_MIDDLE_BUTTON:
        if state==GLUT_DOWN:
            if _g_controller.onMiddleDown(x, y):
                glutPostRedisplay()
        else:
            if _g_controller.onMiddleUp(x, y):
                glutPostRedisplay()
    elif button==GLUT_RIGHT_BUTTON:
        if state==GLUT_DOWN:
            if _g_controller.onRightDown(x, y):
                glutPostRedisplay()
        else:
            if _g_controller.onRightUp(x, y):
                glutPostRedisplay()

    elif button==3:
        if _g_controller.onWheel(-1):
            glutPostRedisplay()

    elif button==4:
        if _g_controller.onWheel(1):
            glutPostRedisplay()

    else:
        logger.warn("unknown mouse:", button, state, x, y)


def _motion(x, y):
    if _g_controller.onMotion(x, y):
        glutPostRedisplay()


def _keyboard(key, x, y):
    if _g_controller.onKeyDown(ord(key)):
        glutPostRedisplay()


def _draw():
    _g_controller.draw()
    glutSwapBuffers()


def _timer(_):
    _g_controller.onUpdate(MSPF)
    glutTimerFunc(MSPF, timer , 0);
    glutPostRedisplay();


def _create_idle_func():
    # nonlocal
    lastclock=[0]
    def idle():
        clock=time.clock()
        d=(clock-lastclock[0])*1000
        _g_controller.onUpdate(d)
        glutPostRedisplay()
        lastclock[0]=clock
    return idle


def mainloop(controller, width: int=640, height: int=480, title: bytearray=b"glut sample"):
    """ [FUNCTIONS] setup and start glut mainloop
    """
    global _g_controller
    _g_controller=controller

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_STENCIL)
    glutInitWindowSize(width, height)
    glutCreateWindow(title)
    # Windowのサイズが変わった時に呼ばれる関数を登録
    glutReshapeFunc(_resize)
    # 描画時に呼ばれる関数を登録
    glutDisplayFunc(_draw)
    # マウスボタン押し上げ時に呼ばれる関数
    glutMouseFunc(_mouse)
    # マウスドラッグ時に呼ばれる関数
    glutMotionFunc(_motion)
    # キーボードが押された時に呼ばれる関数
    glutKeyboardFunc(_keyboard)
    # タイマー
    #glutTimerFunc(MSPF, timer , 0);
    # idle
    glutIdleFunc(_create_idle_func())
    # start mainloop
    glutMainLoop()


if __name__=="__main__":
    import sys
    sys.path.append('..')
    import glglue.sample
    mainloop(glglue.sample.SampleController()
        , width=480, height=480, title=b"glut")
