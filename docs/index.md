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

```{toctree}
samples/wgl
```

### [Windows](./examples/wgl_sample.py)

### [glut](./examples/glut_sample.py)

* require glut.dll or freeglut.dll

### [SDL2](./examples/pysdl2_sample.py)

* require sdl2.dll
* `pip install pysdl2`

### [PyQt5](./examples/qyqt5_sample.py)

* `pip install pyqt5`

### [PySide2](./examples/qyside2_sample.py)

* `pip install pyside2`

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
