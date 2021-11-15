# glglue

<!-- ## minimal usage

* [minimal](./examples/minimal.py)

then implement your own Controller. -->

## Controller convention

You should implement Controller class that has follow methods.

``` py
class Controller:
    def onResize(self, w: int, h: int) -> None:
        ''' when OpenGL window is resized. '''
        pass

    def onLeftDown(self, x: int, y: int) -> None:
        ''' mouse input '''
        pass

    def onLeftUp(self, x: int, y: int) -> None:
        ''' mouse input '''
        pass

    def onMiddleDown(self, x: int, y: int) -> None:
        ''' mouse input '''
        pass

    def onMiddleUp(self, x: int, y: int) -> None:
        ''' mouse input '''
        pass

    def onRightDown(self, x: int, y: int) -> None:
        ''' mouse input '''
        pass

    def onRightUp(self, x: int, y: int) -> None:
        ''' mouse input '''
        pass

    def onMotion(self, x: int, y: int) -> None:
        ''' mouse input '''
        pass

    def onWheel(self, d: int) -> None:
        ''' mouse input '''
        pass

    def onKeyDown(self, keycode: int) -> None:
        ''' keyboard input'''
        pass

    def onUpdate(self, d: int) -> None:
        ''' each frame. milliseconds '''
        pass

    def draw(self) -> None:
        ''' each frame'''
        pass
```

## Samples

同じ `OpenGL Controller` を異なる GUI で使いまわすことができる。

```{toctree}
samples/wgl
samples/glut
samples/pysdl2
samples/pyqt5
samples/pyside6
```

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
