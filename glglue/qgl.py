#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, QtOpenGL


class Widget(QtOpenGL.QGLWidget):
    def __init__(self, parent, controller):
        QtOpenGL.QGLWidget.__init__(
                self, 
                QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers), 
                parent)
        self.controller=controller

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(150, 150)

    def paintGL(self):
        self.controller.draw()

    def resizeGL(self, width, height):
        self.controller.onResize(width, height)

    def mousePressEvent(self, event):
        pos = QtCore.QPoint(event.pos())
        if event.buttons() & QtCore.Qt.LeftButton:
            if self.controller.onLeftDown(pos.x(), pos.y()):
                self.repaint()
        elif event.buttons() & QtCore.Qt.MiddleButton:
            if self.controller.onMiddleDown(pos.x(), pos.y()):
                self.repaint()
        elif event.buttons() & QtCore.Qt.RightButton:
            if self.controller.onRightDown(pos.x(), pos.y()):
                self.repaint()

    def mousePressEvent(self, event):
        pos = QtCore.QPoint(event.pos())
        if event.buttons() & QtCore.Qt.LeftButton:
            if self.controller.onLeftDown(pos.x(), pos.y()):
                self.repaint()
        elif event.buttons() & QtCore.Qt.MiddleButton:
            if self.controller.onMiddleDown(pos.x(), pos.y()):
                self.repaint()
        elif event.buttons() & QtCore.Qt.RightButton:
            if self.controller.onRightDown(pos.x(), pos.y()):
                self.repaint()

    def mouseReleaseEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            if self.controller.onLeftUp(event.x(), event.y()):
                self.repaint()
        elif event.buttons() & QtCore.Qt.MiddleButton:
            if self.controller.onMiddleUp(event.x(), event.y()):
                self.repaint()
        elif event.buttons() & QtCore.Qt.RightButton:
            if self.controller.onRightUp(event.x(), event.y()):
                self.repaint()

    def mouseMoveEvent(self, event):
        self.controller.onMotion(event.x(), event.y())


if __name__=="__main__":
    from PyQt4 import Qt
    import glglue.sample
    class Window(Qt.QWidget):
        def __init__(self, parent=None):
            Qt.QWidget.__init__(self, parent)
            # setup opengl widget
            self.controller=glglue.sample.SampleController()
            self.glwidget=Widget(self, self.controller)
            # packing
            mainLayout = Qt.QHBoxLayout()
            mainLayout.addWidget(self.glwidget)
            self.setLayout(mainLayout)

    import sys
    app = Qt.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

