# glglue

<https://github.com/ousttrue/glglue>

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

## Controller convention

GUI からのイベントを受け取って OpenGL を描画するクラス。

```{gitinclude} HEAD src/glglue/basecontroller.py
:language: python
:caption:
```

## GUI Samples

各種 GUI の使用例

```{toctree}
samples/wgl
samples/glut
samples/pysdl2
samples/pyqt5
samples/pyside6
```

## Controller Samples

Controller の実装例

```{toctree}
controller/gl15
controller/gl33
controller/imgui
```

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
