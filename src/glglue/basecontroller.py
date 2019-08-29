#!/usr/bin/python
# coding: utf-8

import abc


class BaseController(object):
    __metaclass__=abc.ABCMeta
    def __init__(self):
        pass

    @abc.abstractmethod
    def onUpdate(*args):
        """
        updage scene
        """
        pass

    @abc.abstractmethod
    def onLeftDown(self, x, y):
        """
        mouse event
        """
        pass

    @abc.abstractmethod
    def onLeftUp(self, x, y):
        """
        mouse event
        """
        pass

    @abc.abstractmethod
    def onMiddleDown(self, x, y):
        """
        mouse event
        """
        pass

    @abc.abstractmethod
    def onMiddleUp(self, x, y):
        """
        mouse event
        """
        pass

    @abc.abstractmethod
    def onRightDown(self, x, y):
        """
        mouse event
        """
        pass

    @abc.abstractmethod
    def onRightUp(self, x, y):
        """
        mouse event
        """
        pass

    @abc.abstractmethod
    def onMotion(self, x, y):
        """
        mouse event
        """
        pass

    @abc.abstractmethod
    def onResize(self, w, h):
        """
        gui event
        """
        pass

    @abc.abstractmethod
    def onWheel(self, d):
        """
        mouse event
        """
        pass

    @abc.abstractmethod
    def onKeyDown(*args):
        """
        keyboard event
        """
        pass

    @abc.abstractmethod
    def draw(self):
        """
        draw scene
        """
        pass


