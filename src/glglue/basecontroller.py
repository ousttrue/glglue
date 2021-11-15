# coding: utf-8

from abc import ABCMeta, abstractmethod


class BaseController(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def onUpdate(*args):
        """
        updage scene
        """
        pass

    @abstractmethod
    def onLeftDown(self, x: int, y: int):
        """
        mouse event
        """
        pass

    @abstractmethod
    def onLeftUp(self, x: int, y: int):
        """
        mouse event
        """
        pass

    @abstractmethod
    def onMiddleDown(self, x: int, y: int):
        """
        mouse event
        """
        pass

    @abstractmethod
    def onMiddleUp(self, x: int, y: int):
        """
        mouse event
        """
        pass

    @abstractmethod
    def onRightDown(self, x: int, y: int):
        """
        mouse event
        """
        pass

    @abstractmethod
    def onRightUp(self, x: int, y: int):
        """
        mouse event
        """
        pass

    @abstractmethod
    def onMotion(self, x: int, y: int):
        """
        mouse event
        """
        pass

    @abstractmethod
    def onResize(self, w: int, h: int):
        """
        gui event
        """
        pass

    @abstractmethod
    def onWheel(self, d: int):
        """
        mouse event
        """
        pass

    @abstractmethod
    def onKeyDown(*args: str):
        """
        keyboard event
        """
        pass

    @abstractmethod
    def draw(self):
        """
        draw scene
        """
        pass
