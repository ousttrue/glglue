from .camera import Camera, ArcBall, ScreenShift
from .mouse_event import MouseEvent


class MouseCamera:
    def __init__(self, mouse_event: MouseEvent, *, distance: float = 5, y: float = 0) -> None:
        self.camera = Camera(distance=distance, y=y)
        self.mouse_event = mouse_event
        self.mouse_event.bind_right_drag(
            ArcBall(self.camera.view, self.camera.projection))
        self.middle_drag = ScreenShift(
            self.camera.view, self.camera.projection)
        self.mouse_event.bind_middle_drag(self.middle_drag)
        self.mouse_event.wheel += [self.middle_drag.wheel]
