# -*- coding: utf-8 -*-
import logging
from PySide6 import QtCore, QtGui, QtOpenGLWidgets, QtWidgets
from .basecontroller import BaseController


class Widget(QtOpenGLWidgets.QOpenGLWidget):
    '''
    https://doc.qt.io/qtforpython/PySide6/QtOpenGLWidgets/QOpenGLWidget.html
    '''

    def __init__(self, parent, controller: BaseController, dpi_scale=1.0, core_profile=True):
        super().__init__(parent)
        self.controller = controller
        self.setMouseTracking(True)
        self.dpi_Scale = dpi_scale

        if core_profile:
            format = QtGui.QSurfaceFormat()
            format.setDepthBufferSize(24)
            format.setStencilBufferSize(8)
            format.setVersion(3, 2)
            format.setProfile(QtGui.QSurfaceFormat.CoreProfile)
            # self.setFormat(format)
            QtGui.QSurfaceFormat.setDefaultFormat(format)
            # must be called before the widget or its parent window gets shown

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


class CustomLogger(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)

        if record.levelno == logging.DEBUG:
            msg = f'<font color="gray">{msg}</font><br>'
        elif record.levelno == logging.WARNING:
            msg = f'<font color="orange">{msg}</font><br>'
        elif record.levelno == logging.ERROR:
            msg = f'<font color="red">{msg}</font><br>'
        else:
            msg = f'{msg}<br>'

        self.widget.textCursor().movePosition(QtGui.QTextCursor.Start)
        self.widget.textCursor().insertHtml(msg)

    def write(self, m):
        pass

class QPlainTextEditLogger(QtWidgets.QPlainTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.setReadOnly(True)
        self.log_handler = CustomLogger(self)
