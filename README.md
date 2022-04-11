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

And OpenGL utilities.

## Requirements

* Python 3.10

## Site

* <https://ousttrue.github.io/glglue/>
* <https://pypi.python.org/pypi/glglue/>
