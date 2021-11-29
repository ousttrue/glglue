# glglue

The glue code which mediates between OpenGL and some GUI.

GUI イベント(resize, mouse, keyboard, repaint) を OpenGL に橋渡しする。

```                           
GUI                         OpenGL controller
+--------+                   +------------+
| win32  |--window resize--->| Update     |
| glut   |--mouse input----->| Update     |
| sdl    |--keyboard input-->| Update     |
| pyside6|                   |            |
|     etc|--repaint--------->| Draw       |
+--------+                   +------------+
```

## Requirements

* Python 3.10

## Site

* <https://ousttrue.github.io/glglue/>
* <https://pypi.python.org/pypi/glglue/>

## TODO

* [x] scene: node transform
* [x] pyside6: logger
* [ ] pyside6: loop framerate

## History

* 20211121 1.5.0 scene and renderer. planar and interleaved VBO.
* 20211117 1.4.0 update VBO, IBO. add VAO.
* 20211115 1.3.2 add ImGuiController
* 20211115 1.3.0 Update BaseController. Returns whether redraw is required.
* 20211115 1.2.0 remove PySide2 and add PySide6. fix wgl.
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
$ py -m venv .venv
$ .venv/Scripts/Activate.ps1
(.venv)$ pip install -e .
```
