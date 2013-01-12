glglue is the glue code which mediates between OpenGL and some GUI

Requirements
============
* Python 2.7
* Python 3.2

Features
========
* glut window
* tkinter's togl widget
* wxPython's GLCanvas widget(wxPython for python3 is not exist)
* pyQt4's qgl widget
* win32api wgl

Site
====
* http://pypi.python.org/pypi/glglue/
* https://github.com/ousttrue/glglue

Controller convention
=====================
You should implement Controller class that has follow methods.

* onUpdate
* onLeftDown
* onLeftUp
* onMiddleDown
* onMiddleUp
* onRightDown
* onRightUp
* onMotion
* onResize
* onWheel
* onKeyDown
* draw

example

::

    # coding: utf-8
    from OpenGL.GL import *
    
    
    class Controller(object):
        def __init__(self):
            pass
    
        def onResize(self, w, h):
            glViewport(0, 0, w, h)
    
        def onLeftDown(self, x, y):
            print 'onLeftDown', x, y
    
        def onLeftUp(self, x, y):
            print 'onLeftUp', x, y
    
        def onMiddleDown(self, x, y):
            print 'onMiddleDown', x, y
    
        def onMiddleUp(self, x, y):
            print 'onMiddleUp', x, y
    
        def onRightDown(self, x, y):
            print 'onRightDown', x, y
    
        def onRightUp(self, x, y):
            print 'onRightUp', x, y
    
        def onMotion(self, x, y):
            print 'onMotion', x, y
    
        def onWheel(self, d):
            print 'onWheel', d
    
        def onKeyDown(self, keycode):
            print 'onKeyDown', keycode
    
        def onUpdate(self, d):
            print 'onUpdate', d
    
        def draw(self):
            glClearColor(0.9, 0.5, 0.0, 0.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
            glBegin(GL_TRIANGLES)
            glVertex(-1.0,-1.0)
            glVertex( 1.0,-1.0)
            glVertex( 0.0, 1.0)
            glEnd()
    
            glFlush()
    
    
    if __name__=="__main__":
        controller=Controller()
        import glglue.glut
        glglue.glut.mainloop(controller, width=640, height=480, title="sample")    
        #import glglue.wgl
        #glglue.wgl.mainloop(controller, width=640, height=480, title="sample")


Samples
=======

glut
----
requrie pyOpenGL + glut install

glut install on Windows
~~~~~~~~~~~~~~~~~~~~~~~
1) download glut-3.7.6-bin.zip from http://user.xmission.com/~nate/glut.html
2) copy glut32.dll to C:/PythonXX/

::

    import glglue.sample
    import glglue.glut

    if __name__=="__main__":
        controller=glglue.sample.SampleController()
        glglue.glut.mainloop(controller)

tkinter
-------
requrie pyOpenGL + togl install

Togl install on Windows
~~~~~~~~~~~~~~~~~~~~~~~
1) download Togl2.0-8.4-Windows.zip from http://sourceforge.net/projects/togl/files/Togl/2.0/
2) copy Togl2.0-8.4-Windows/lib/Togl2.0 to C:/PythonXX/tcl/Togl2.0

::

    import sys
    import Tkinter as tkinter
    import glglue.togl
    import glglue.sample
    class Frame(tkinter.Frame):
        def __init__(self, width, height, master=None, **kw):
            #super(Frame, self).__init__(master, **kw)
            tkinter.Frame.__init__(self, master, **kw)
            # setup opengl widget
            self.controller=glglue.sample.SampleController()
            self.glwidget=glglue.togl.Widget(
                    self, self.controller, width=width, height=height)
            self.glwidget.pack(fill=tkinter.BOTH, expand=True)
            # event binding(require focus)
            self.bind('<Key>', self.onKeyDown)
            self.bind('<MouseWheel>', lambda e: self.controller.onWheel(-e.delta) and self.glwidget.onDraw())

        def onKeyDown(self, event):
            key=event.keycode
            if key==27:
                # Escape
                sys.exit()
            if key==81:
                # q
                sys.exit()
            else:
                print("keycode: %d" % key)

    f = Frame(width=600, height=600)
    f.pack(fill=tkinter.BOTH, expand=True)
    f.focus_set()
    f.mainloop()

wxPython
--------
require pyOpenGL + wxPython

::

    import wx
    import glglue.sample
    import glglue.wxglcanvas
    class Frame(wx.Frame):
        def __init__(self, parent, **kwargs):
            super(Frame, self).__init__(parent, **kwargs)
            # setup opengl widget
            self.controller=glglue.sample.SampleController()
            self.glwidget=glglue.wxglcanvas.Widget(self, self.controller)
            # packing
            sizer=wx.BoxSizer(wx.HORIZONTAL)
            self.SetSizer(sizer)
            sizer.Add(self.glwidget, 1, wx.EXPAND)

    app = wx.App(False)
    frame=Frame(None, title='glglue')
    frame.Show()
    app.MainLoop()

pyQt4
-----
require pyOpenGL + pyQt4

::

    from PyQt4 import Qt
    import glglue.sample
    import glglue.qgl
    class Window(Qt.QWidget):
        def __init__(self, parent=None):
            Qt.QWidget.__init__(self, parent)
            # setup opengl widget
            self.controller=glglue.sample.SampleController()
            self.glwidget=glglue.qgl.Widget(self, self.controller)
            # packing
            mainLayout = Qt.QHBoxLayout()
            mainLayout.addWidget(self.glwidget)
            self.setLayout(mainLayout)

    import sys
    app = Qt.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

pyGame
------
require pyOpenGL + pyGame

::

    import pygame
    from pygame.locals import *
    import glglue.sample
    
    if __name__=="__main__":   
        pygame.init()
        size=(640, 480)
        pygame.display.gl_set_attribute(pygame.GL_STENCIL_SIZE, 2)
        screen = pygame.display.set_mode(size, 
                HWSURFACE | OPENGL | DOUBLEBUF)
    
        controller=glglue.sample.SampleController()
        controller.onResize(*size)
    
        clock = pygame.time.Clock()    
        is_running=True
        while is_running:
            #pressed = pygame.key.get_pressed()
    
            # event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    is_running=False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        is_running=False
                    else:
                        controller.onKeyDown(event.key)
                
            # update
            d = clock.tick()
            if d>0:
                controller.onUpdate(d)
                controller.draw()
                pygame.display.flip()

win32api
--------
require pyOpenGL + pywin32(win32con)

pywin32(win32con) install on Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1) download pywin32-xxx.exe from http://sourceforge.net/projects/pywin32/files/pywin32/
2) execute installer

::

    import glglue.sample
    import glglue.wgl
    
    if __name__=="__main__":
        factory=glglue.wgl.WindowFactory()
        window=factory.create(glglue.wgl.Window, title="sample")
        window.createGLContext(16)
        window.controller=glglue.sample.SampleController()
        window.show()
        import sys
        sys.exit(factory.loop())

short smaple

::

    import glglue.sample
    import glglue.wgl

    if __name__=="__main__":
        controller=glglue.sample.SampleController()
        glglue.wgl.mainloop(controller, width=640, height=480, title="sample")

History
=======
* 20130113 0.3.1 fix mouse manupilation for PyQt4
* 20120127 0.3.0 add mouse manupilation
* 20120127 0.2.6 add stencil buffer for glut/wgl/sdl sample
* 20120126 0.2.5 use glutIdleFunc for glut animation
* 20120125 0.2.4 add wgl/sdl animation
* 20120124 0.2.3 add glut animation
* 20120123 0.2.2 add glut width, height prameter
* 20120119 0.2.0 python3 support
* 20120119 0.1.3 add SetFocus when mouseDown on wxglcanvas
* 20120115 0.1.2 update README. add MANIFEST.in
* 20120114 0.1.1 update README
* 20120114 0.1.0 implement wxglcanvas mouse event and keyboard event handling
* 20120113 0.0.9 fix wxglcanvas
* 20120112 0.0.8 fix lacking of README.rst
* 20111230 0.0.7 add wgl.mainloop, implement wgl mouse callback
* 20111230 0.0.4 fix SetWindowLongPtr
* 20111229 0.0.3 include glglue.sample. add wgl

