# glglue

- <https://ousttrue.github.io/glglue/>
- <https://pypi.python.org/pypi/glglue/>

The glue code which mediates between OpenGL and some GUI.
GUI イベント(resize, mouse, keyboard, repaint) を OpenGL に橋渡しする。

```
GUI                         OpenGL controller
+--------+                   +------------+
| win32  |--window resize--->| Update     |
| glut   |--mouse input----->| Update     |
| sdl    |--keyboard input-->| Update     |
| pyside6|                   |            |
| gtk3   |--repaint--------->| Draw       |
| gtk4   |                   +------------+
+--------+
```

And OpenGL utilities.

## Requirements

- Python 3.11

## status

| platform | status | comment                                  |
| -------- | ------ | ---------------------------------------- |
| glut     | ok     | windows11, PATH to freeglut64.vc.dll     |
| glfw     | ok     | windows11, pip install glfw              |
| gtk3     | ?      | require gtk3 self build                  |
| gtk4     | ?      | require gtk4 self build                  |
| sdl2     | ok     | windows11, pip install pysdl2 pysdl2-dll |
| qt6      | ok     | windows11, pip install pyside6)          |
| win32    | ok     | windows11                                |
