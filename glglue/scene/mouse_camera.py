from .camera import Camera, ArcBall, ScreenShift
from .mouse_event import MouseEvent
from glglue.frame_input import FrameInput


class MouseCamera:
    def __init__(self, *, distance: float = 5, y: float = 0) -> None:
        self.camera = Camera(distance=distance, y=y)
        self.mouse_event = MouseEvent()
        self.mouse_event.bind_right_drag(
            ArcBall(self.camera.view, self.camera.projection)
        )
        self.middle_drag = ScreenShift(self.camera.view, self.camera.projection)
        self.mouse_event.bind_middle_drag(self.middle_drag)
        self.mouse_event.wheel += [self.middle_drag.wheel]

    def process(self, frame: FrameInput):
        self.camera.projection.resize(frame.width, frame.height)
        self.mouse_event.process(frame)
