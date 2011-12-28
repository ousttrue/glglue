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
    def onLeftDown(*args):
        """
        mouse event
        """
        pass

    @abc.abstractmethod
    def onLeftUp(*args):
        """
        mouse event
        """
        pass

    @abc.abstractmethod
    def onMiddleDown(*args):
        """
        mouse event
        """
        pass

    @abc.abstractmethod
    def onMiddleUp(*args):
        """
        mouse event
        """
        pass

    @abc.abstractmethod
    def onRightDown(*args):
        """
        mouse event
        """
        pass

    @abc.abstractmethod
    def onRightUp(*args):
        """
        mouse event
        """
        pass

    @abc.abstractmethod
    def onMotion(*args):
        """
        mouse event
        """
        pass

    @abc.abstractmethod
    def onResize(*args):
        """
        gui event
        """
        pass

    @abc.abstractmethod
    def onWheel(*args):
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


