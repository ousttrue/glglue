# glglue

<https://github.com/ousttrue/glglue>

GUI イベント(resize, mouse, keyboard, repaint) を OpenGL に橋渡しする。

```                           
GUI
+--------+
| win32  |
| glut   |
| sdl    |
| pyside6|
| gtk3   |----FrameInput----> RenderFunc
| gtk4   |     elapsed_time  
+--------+     window.width
               window.height
               mouse.x
               mouse.y
               mouse.left_down
               mouse.right_down
               mouse.middle_down
               mouse.wheel
```

## FrameInput

`Version 2.0`

Frame 毎の GUI イベントをまとめた。

```python
    def render(self, frame: glglue.frame_input.FrameInput):
        '''
        ユーザーはこの関数を実装する。
        '''
        GL.glClear()
        # ...
        GL.glFlush()
```

## GUI MainLoop

* pysdie6
* gtk3
* gtk4

## User MainLoop

* freeglut
* glfw
* pysdl2
* wgl
