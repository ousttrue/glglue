======
glglue
======
glglueは、PyOpenGLとWindowSystemを分離しようという趣旨のユーティリティです。
python2はサポートしないことにした。

Requirements
============
* Python 3.2

Features
========
* glut window
* pyQt4's qgl widget
* win32api wgl

Site
====
* http://pypi.python.org/pypi/glglue/
* https://github.com/ousttrue/glglue

Samples
=======
show tutorial and examples directory.

Controller convention
=====================
You should implement Controller class that has follow methods.

* onUpdate
* onLeftDown
* onLeftUp
* onMiddleDown
* onMiddleUp
* onRightDown
* onRightUp
* onMotion
* onResize
* onWheel
* onKeyDown
* draw


# History

* 20160417 0.4.1 remove print. use logger
* 20160318 0.4 fix for python3. drop python2 support
* 20130113 0.3.1 fix mouse manupilation for PyQt4
* 20120127 0.3.0 add mouse manupilation
* 20120127 0.2.6 add stencil buffer for glut/wgl/sdl sample
* 20120126 0.2.5 use glutIdleFunc for glut animation
* 20120125 0.2.4 add wgl/sdl animation
* 20120124 0.2.3 add glut animation
* 20120123 0.2.2 add glut width, height prameter
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

