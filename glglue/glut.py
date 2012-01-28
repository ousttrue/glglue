#!/usr/bin/python
# coding: utf-8

from OpenGL.GLUT import *
import time

# このソースではOpenGL操作をしない
#from OpenGL.GL import *

FPS=30
MSPF=int(1000.0/FPS)

# OpenGL処理用のglobal変数
# glutのコールバック関数に来たイベントをここに丸投げする
g_controller=None


def resize(w, h):
    g_controller.onResize(w, h)


def mouse(button, state, x, y):
    # マウスイベントの振り分けはここでしてしまう
    # g_controllerのメソッドからTrueが返ったら再描画する
    if button==GLUT_LEFT_BUTTON:
        if state==GLUT_DOWN:
            if g_controller.onLeftDown(x, y):
                glutPostRedisplay()
        else:
            if g_controller.onLeftUp(x, y):
                glutPostRedisplay()
    elif button==GLUT_MIDDLE_BUTTON:
        if state==GLUT_DOWN:
            if g_controller.onMiddleDown(x, y):
                glutPostRedisplay()
        else:
            if g_controller.onMiddleUp(x, y):
                glutPostRedisplay()
    elif button==GLUT_RIGHT_BUTTON:
        if state==GLUT_DOWN:
            if g_controller.onRightDown(x, y):
                glutPostRedisplay()
        else:
            if g_controller.onRightUp(x, y):
                glutPostRedisplay()

    elif button==3:
        if g_controller.onWheel(-1):
            glutPostRedisplay()

    elif button==4:
        if g_controller.onWheel(1):
            glutPostRedisplay()

    else:
        print("unknown mouse:", button, state, x, y)


def motion(x, y):
    if g_controller.onMotion(x, y):
        glutPostRedisplay()


def keyboard(key, x, y):
    if g_controller.onKeyDown(ord(key)):
        glutPostRedisplay()


def draw():
    g_controller.draw()
    glutSwapBuffers()


def timer(_):
    g_controller.onUpdate(MSPF)
    glutTimerFunc(MSPF, timer , 0);
    glutPostRedisplay();


def create_idle_func():
    # nonlocal
    lastclock=[0]
    def idle():
        clock=time.clock()
        d=(clock-lastclock[0])*1000
        g_controller.onUpdate(d)
        glutPostRedisplay()
        lastclock[0]=clock
    return idle

 
def mainloop(controller, width=640, height=480, title=b"glut sample"):
    global g_controller
    g_controller=controller

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_STENCIL)
    glutInitWindowSize(width, height)
    glutCreateWindow(title)
    # Windowのサイズが変わった時に呼ばれる関数を登録
    glutReshapeFunc(resize)
    # 描画時に呼ばれる関数を登録
    glutDisplayFunc(draw)
    # マウスボタン押し上げ時に呼ばれる関数
    glutMouseFunc(mouse)
    # マウスドラッグ時に呼ばれる関数
    glutMotionFunc(motion)
    # キーボードが押された時に呼ばれる関数
    glutKeyboardFunc(keyboard)
    # タイマー 
    #glutTimerFunc(MSPF, timer , 0);
    # idle       
    glutIdleFunc(create_idle_func())

    glutMainLoop()


if __name__=="__main__":
    import glglue.sample
    mainloop(glglue.sample.SampleController(), width=480, height=480, title=b"glut")

