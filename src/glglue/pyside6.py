# -*- coding: utf-8 -*-
from PySide6 import QtCore
from PySide6 import QtOpenGLWidgets
from .basecontroller import BaseController


class Widget(QtOpenGLWidgets.QOpenGLWidget):
    '''
    https://doc.qt.io/qtforpython/PySide6/QtOpenGLWidgets/QOpenGLWidget.html
    '''

    def __init__(self, parent, controller: BaseController, dpi_scale=1.0):
        super().__init__(parent)
        self.controller = controller
        self.setMouseTracking(True)
        self.dpi_Scale = dpi_scale

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(150, 150)

    def paintGL(self):
        self.controller.draw()

    def resizeGL(self, width, height):
        if self.controller.onResize(int(width * self.dpi_Scale), int(height * self.dpi_Scale)):
            self.repaint()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.controller.onLeftDown(event.x() * self.dpi_Scale, event.y() * self.dpi_Scale):
                self.repaint()
        elif event.button() == QtCore.Qt.MiddleButton:
            if self.controller.onMiddleDown(event.x() * self.dpi_Scale, event.y() * self.dpi_Scale):
                self.repaint()
        elif event.button() == QtCore.Qt.RightButton:
            if self.controller.onRightDown(event.x() * self.dpi_Scale, event.y() * self.dpi_Scale):
                self.repaint()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.controller.onLeftUp(event.x() * self.dpi_Scale, event.y() * self.dpi_Scale):
                self.repaint()
        elif event.button() == QtCore.Qt.MiddleButton:
            if self.controller.onMiddleUp(event.x() * self.dpi_Scale, event.y() * self.dpi_Scale):
                self.repaint()
        elif event.button() == QtCore.Qt.RightButton:
            if self.controller.onRightUp(event.x() * self.dpi_Scale, event.y() * self.dpi_Scale):
                self.repaint()

    def mouseMoveEvent(self, event):
        if self.controller.onMotion(event.x() * self.dpi_Scale, event.y() * self.dpi_Scale):
            self.repaint()

    def wheelEvent(self, event):
        if self.controller.onWheel(-event.angleDelta().y()):
            self.repaint()
