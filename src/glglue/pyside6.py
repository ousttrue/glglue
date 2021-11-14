#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide6 import QtCore, QtGui
from PySide6 import QtOpenGLWidgets


class Widget(QtOpenGLWidgets.QOpenGLWidget):
    '''
    https://doc.qt.io/qtforpython/PySide6/QtOpenGLWidgets/QOpenGLWidget.html
    '''
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(150, 150)

    def paintGL(self):
        self.controller.draw()

    def resizeGL(self, width, height):
        self.controller.onResize(width, height)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.controller.onLeftDown(event.x(), event.y()):
                self.repaint()
        elif event.button() == QtCore.Qt.MiddleButton:
            if self.controller.onMiddleDown(event.x(), event.y()):
                self.repaint()
        elif event.button() == QtCore.Qt.RightButton:
            if self.controller.onRightDown(event.x(), event.y()):
                self.repaint()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.controller.onLeftUp(event.x(), event.y()):
                self.repaint()
        elif event.button() == QtCore.Qt.MiddleButton:
            if self.controller.onMiddleUp(event.x(), event.y()):
                self.repaint()
        elif event.button() == QtCore.Qt.RightButton:
            if self.controller.onRightUp(event.x(), event.y()):
                self.repaint()

    def mouseMoveEvent(self, event):
        if self.controller.onMotion(event.x(), event.y()):
            self.repaint()

    def wheelEvent(self, event):
        if self.controller.onWheel(-event.delta()):
            self.repaint()


if __name__ == "__main__":
    import glglue.sample

    class Window(QtGui.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            # setup opengl widget
            self.controller = glglue.sample.SampleController()
            self.glwidget = Widget(self, self.controller)
            # packing
            mainLayout = QtGui.QHBoxLayout()
            mainLayout.addWidget(self.glwidget)
            self.setLayout(mainLayout)

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
