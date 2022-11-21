import glglue.frame_input


def render(frame: glglue.frame_input.FrameInput):
    from OpenGL import GL

    GL.glViewport(0, 0, frame.width, frame.height)

    r = float(frame.x) / float(frame.width)
    g = 1 if frame.left_down else 0
    if frame.height == 0:
        return
    b = float(frame.y) / float(frame.height)
    GL.glClearColor(r, g, b, 1.0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)  # type: ignore

    GL.glFlush()


def main():
    import glglue.glfw

    loop = glglue.glfw.LoopManager(title="glfw sample")
    while True:
        frame = loop.begin_frame()
        if not frame:
            break
        render(frame)
        loop.end_frame()


if __name__ == "__main__":
    main()
