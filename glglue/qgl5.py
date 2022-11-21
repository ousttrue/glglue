#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtOpenGL


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
        if event.button()==QtCore.Qt.LeftButton:
            if self.controller.onLeftDown(event.x(), event.y()):
                self.repaint()
        elif event.button()==QtCore.Qt.MiddleButton:
            if self.controller.onMiddleDown(event.x(), event.y()):
                self.repaint()
        elif event.button()==QtCore.Qt.RightButton:
            if self.controller.onRightDown(event.x(), event.y()):
                self.repaint()

    def mouseReleaseEvent(self, event):
        if event.button()==QtCore.Qt.LeftButton:
            if self.controller.onLeftUp(event.x(), event.y()):
                self.repaint()
        elif event.button()==QtCore.Qt.MiddleButton:
            if self.controller.onMiddleUp(event.x(), event.y()):
                self.repaint()
        elif event.button()==QtCore.Qt.RightButton:
            if self.controller.onRightUp(event.x(), event.y()):
                self.repaint()

    def mouseMoveEvent(self, event):
        if self.controller.onMotion(event.x(), event.y()):
            self.repaint()

    def wheelEvent(self, event):
        if self.controller.onWheel(-event.angleDelta().y()):
            self.repaint()


if __name__=="__main__":
    from PyQt5 import Qt
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

