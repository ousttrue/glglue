#!/usr/bin/python
# coding: utf-8

from OpenGL.GL import *
from OpenGL.GLU import *


class TargetView(object):
    def __init__(self, distance=None):
        # screen size
        self.w=1
        self.h=1
        # mouse status
        self.x=0
        self.y=0
        self.isLeftDown=False
        self.isMiddleDown=False
        self.isRightDown=False
        # target view params
        self.distance=distance or 5
        self.head=0
        self.pitch=0
        self.shift_x=0
        self.shift_y=0
        self.shift_factor=0.8
        # perspective projection params
        self.fovy=30
        self.aspect=1
        self.near=0.1
        self.far=100

    def updateProjection(self):
        gluPerspective(self.fovy, self.aspect, self.near, self.far)

    def updateView(self):
        glTranslate(self.shift_x, self.shift_y, -self.distance)
        glRotate(self.pitch, 1, 0, 0)
        glRotate(self.head, 0, 1, 0)

    def onResize(self, w=None, h=None):
        print("resize: %d, %d" % (self.w, self.h))
        self.w=w or self.w
        self.h=h or self.h
        glViewport(0, 0, self.w, self.h)
        self.aspect=self.w / float(self.h)

    def onLeftDown(self, x, y):
        self.isLeftDown=True
        self.x=x
        self.y=y

    def onLeftUp(self, x, y):
        self.isLeftDown=False

    def onMiddleDown(self, x, y):
        self.isMiddleDown=True
        self.x=x
        self.y=y

    def onMiddleUp(self, x, y):
        self.isMiddleDown=False

    def onRightDown(self, x, y):
        self.isRightDown=True
        self.x=x
        self.y=y

    def onRightUp(self, x, y):
        self.isRightDown=False

    def onMotion(self, x, y):
        isUpdated=False
        dx=x-self.x
        dy=y-self.y
        if self.isLeftDown:
            if dy>0:
                self.distance*=1.1
            else:
                self.distance*=0.9
            isUpdated=True
        if self.isMiddleDown:
            self.shift_x+=dx / float(self.w) * self.shift_factor * self.distance
            self.shift_y-=dy / float(self.h) * self.shift_factor * self.distance
            isUpdated=True
        if self.isRightDown:
            self.head+=dx
            self.pitch+=dy
            isUpdated=True
        self.x=x
        self.y=y
        return isUpdated

    def onWheel(self, d):
        if d>0:
            self.distance*=1.1
            return True
        elif d<0:
            self.distance*=0.9
            return True

    def printMatrix(self, m):
        print(m[0][0], m[0][1], m[0][2], m[0][3])
        print(m[1][0], m[1][1], m[1][2], m[1][3])
        print(m[2][0], m[2][1], m[2][2], m[2][3])
        print(m[3][0], m[3][1], m[3][2], m[3][3])

