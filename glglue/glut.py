#!/usr/bin/python
# coding: utf-8

from OpenGL.GLUT import *

# このソースではOpenGL操作をしない
#from OpenGL.GL import *

# OpenGL処理用のglobal変数
# glutのコールバック関数に来たイベントをここに丸投げする
g_controller=None


def resize(w, h):
    global g_controller
    g_controller.onResize(w, h)


def mouse(button, state, x, y):
    global g_controller

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
        print "unknown mouse:", button, state, x, y


def motion(x, y):
    global g_controller
    if g_controller.onMotion(x, y):
        glutPostRedisplay()


def keyboard(key, x, y):
    if key=='\033':
        # Escape
        sys.exit()
    if key=='q':
        # q
        sys.exit()
    else:
        print(key)


def draw():
    global g_controller
    g_controller.draw()
    glutSwapBuffers()


def mainloop(controller):
    global g_controller
    g_controller=controller

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutCreateWindow("glut sample")
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

    glutMainLoop()


if __name__=="__main__":
    import glglue.sample
    mainloop(glglue.sample.SampleController())

