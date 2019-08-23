# glglue

The glue code which mediates between OpenGL and some GUI

## Requirements

* Python 3.2

## Site

* http://pypi.python.org/pypi/glglue/
* https://github.com/ousttrue/glglue

## minimal usage

* [minimal](./examples/minimal.py)

then implement your own Controller.

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

## implementations

### maintenance

* [Windows](./examples/wgl_sample.py)
* [glut](./examples/glut_sample.py)
* [SDL2](./examples/pysdl2_sample.py)

* [PyQt5](./examples/qyqt5_sample.py)
* [PySide2](./examples/qyside2_sample.py)

### not maintenance

* [tkinter](./examples/tkinter_sample.py)
* [PyQt4](./examples/pyqt4_sample.py)
* [PySide](./examples/pyside_sample.py)
* wxglcanvas

## History

* 20190824 1.1.0 add PySide2
* 20190824 1.0.0 README.rst to README.md
* 20170926 0.4.4 add PySide
* 20170730 0.4.3 add PySDL2
* 20170726 0.4.2 add PyQt5
* 20160417 0.4.1 remove print. use logger
* 20160318 0.4 fix for python3. drop python2 support
* 20130113 0.3.1 fix mouse manipulation for PyQt4
* 20120127 0.3.0 add mouse manipulation
* 20120127 0.2.6 add stencil buffer for glut/wgl/sdl sample
* 20120126 0.2.5 use glutIdleFunc for glut animation
* 20120125 0.2.4 add wgl/sdl animation
* 20120124 0.2.3 add glut animation
* 20120123 0.2.2 add glut width, height parameter
* 20120119 0.2.0 python3 support
* 20120119 0.1.3 add SetFocus when mouseDown on wxglcanvas
* 20120115 0.1.2 update README. add MANIFEST.in
* 20120114 0.1.1 update README
* 20120114 0.1.0 implement wxglcanvas mouse event and keyboard event handling
* 20120113 0.0.9 fix wxglcanvas
* 20120112 0.0.8 fix lacking of README.rst
* 20111230 0.0.7 add wgl.mainloop, implement wgl mouse callback
* 20111230 0.0.4 fix SetWindowLongPtr
* 20111229 0.0.3 include glglue.sample. add wgl

## maintenance

```
$ python setup.py sdist
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/glglue-1.0.0.tar.gz
```
