import re
from OpenGL.GL import *

from ..basecontroller import BaseController
from . import baseview
from . import triangle

DELEGATE_PATTERN=re.compile('^on[A-Z]')

class SampleController(BaseController):
    def __init__(self, view=None, root=None):
        view=view or baseview.BaseView()
        root=root or triangle.Triangle(0.5)
        self.view=view
        self.root=root
        self.isInitialized=False
        self.delegate(view)
        self.delegate(root)

    def delegate(self, to):
        for name in dir(to):  
            if DELEGATE_PATTERN.match(name):
                method = getattr(to, name)  
                setattr(self, name, method)

    def onUpdate(*args):
        pass

    def onLeftDown(*args):
        pass

    def onLeftUp(*args):
        pass

    def onMiddleDown(*args):
        pass

    def onMiddleUp(*args):
        pass

    def onRightDown(*args):
        pass

    def onRightUp(*args):
        pass

    def onMotion(*args):
        pass

    def onResize(self, w, h):
        pass

    def onWheel(*args):
        pass

    def onKeyDown(self, key):
        print("onKeyDown: %x" % key)

    def onInitialize(*args):
        pass

    def initilaize(self):
        self.view.onResize()
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.4, 0.0)
        # 初期化時の呼び出し
        self.onInitialize()

    def draw(self):
        if not self.isInitialized:
            self.initilaize()
            self.isInitialized=True
        # OpenGLバッファのクリア
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # 投影行列のクリア
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.view.updateProjection()
        # モデルビュー行列のクリア
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # OpenGL描画
        self.view.updateView()
        self.root.draw()
        glFlush()

