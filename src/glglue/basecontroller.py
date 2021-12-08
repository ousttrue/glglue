# coding: utf-8

from abc import ABCMeta, abstractmethod


class BaseController(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def onUpdate(*args) -> bool:
        """
        Update scene. Returns whether redraw is required.
        """
        return False

    @abstractmethod
    def onLeftDown(self, x: int, y: int) -> bool:
        """
        Mouse event. Returns whether redraw is required.
        """
        return False

    @abstractmethod
    def onLeftUp(self, x: int, y: int) -> bool:
        """
        Mouse event. Returns whether redraw is required.
        """
        return False

    @abstractmethod
    def onMiddleDown(self, x: int, y: int) -> bool:
        """
        Mouse event. Returns whether redraw is required.
        """
        return False

    @abstractmethod
    def onMiddleUp(self, x: int, y: int) -> bool:
        """
        Mouse event. Returns whether redraw is required.
        """
        return False

    @abstractmethod
    def onRightDown(self, x: int, y: int) -> bool:
        """
        Mouse event. Returns whether redraw is required.
        """
        return False

    @abstractmethod
    def onRightUp(self, x: int, y: int) -> bool:
        """
        Mouse event. Returns whether redraw is required.
        """
        return False

    @abstractmethod
    def onMotion(self, x: int, y: int) -> bool:
        """
        Mouse event. Returns whether redraw is required.
        """
        return False

    @abstractmethod
    def onResize(self, w: int, h: int) -> bool:
        """
        Gui event. Returns whether redraw is required.
        """
        return False

    @abstractmethod
    def onWheel(self, d: int) -> bool:
        """
        Mouse event. Returns whether redraw is required.
        """
        return False

    @abstractmethod
    def onKeyDown(self, *args: str) -> bool:
        """
        Keyboard event. Returns whether redraw is required.
        """
        return False

    @abstractmethod
    def draw(self) -> None:
        """
        draw scene
        """
        pass
