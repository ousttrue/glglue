#!/usr/bin/python
# coding: utf-8

from OpenGL.GLUT import *

# このソースではOpenGL操作をしない
#from OpenGL.GL import *

# OpenGL処理用のglobal変数
# glutのコールバック関数に来たイベントをここに丸投げする
g_engine=None


def resize(w, h):
    global g_engine
    g_engine.onResize(w, h)


def mouse(button, state, x, y):
    global g_engine

    # マウスイベントの振り分けはここでしてしまう
    # g_engineのメソッドからTrueが返ったら再描画する
    if button==GLUT_LEFT_BUTTON:
        if state==GLUT_DOWN:
            if g_engine.onLeftDown(x, y):
                glutPostRedisplay()
        else:
            if g_engine.onLeftUp(x, y):
                glutPostRedisplay()
    elif button==GLUT_MIDDLE_BUTTON:
        if state==GLUT_DOWN:
            if g_engine.onMiddleDown(x, y):
                glutPostRedisplay()
        else:
            if g_engine.onMiddleUp(x, y):
                glutPostRedisplay()
    elif button==GLUT_RIGHT_BUTTON:
        if state==GLUT_DOWN:
            if g_engine.onRightDown(x, y):
                glutPostRedisplay()
        else:
            if g_engine.onRightUp(x, y):
                glutPostRedisplay()

    elif button==3:
        if g_engine.onWheel(-1):
            glutPostRedisplay()

    elif button==4:
        if g_engine.onWheel(1):
            glutPostRedisplay()

    else:
        print "unknown mouse:", button, state, x, y


def motion(x, y):
    global g_engine
    if g_engine.onMotion(x, y):
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
    global g_engine
    g_engine.draw()
    glutSwapBuffers()


def mainloop(engine):
    global g_engine
    g_engine=engine

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

