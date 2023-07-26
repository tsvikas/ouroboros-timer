import time

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.widget import Widget

DEBUG_SPEED = None
DEBUG_START_SECONDS = None

RESET_SECONDS = 1
WORK_MINUTES = 25
BREAK_MINUTES = 5
FPS = 60

MINUTE = 60
DEGREES = 360
WORK_SECONDS = WORK_MINUTES * MINUTE / (DEBUG_SPEED or 1)
BREAK_SECONDS = BREAK_MINUTES * MINUTE / (DEBUG_SPEED or 1)
TOTAL_CYCLE_SECONDS = WORK_SECONDS + BREAK_SECONDS


class TimerBG(Widget):
    switch_angle = NumericProperty(WORK_SECONDS / TOTAL_CYCLE_SECONDS * DEGREES)


class TimerCircle(Widget):
    start_percentage = NumericProperty(0)
    end_percentage = NumericProperty(0)


class TimerCanvas(Widget):
    seconds = NumericProperty(0)
    remaining_seconds = NumericProperty(0)
    remaining_seconds_in_stage = NumericProperty(0)
    circle_fg = ObjectProperty(None)
    circle_size = NumericProperty(0)
    debug_interval = NumericProperty(
         0 if DEBUG_START_SECONDS is None else (DEBUG_START_SECONDS - time.time())
    )

    def update(self, dt):
        self.seconds = (time.time() + self.debug_interval) % TOTAL_CYCLE_SECONDS
        self.remaining_seconds = TOTAL_CYCLE_SECONDS - self.seconds
        self.remaining_seconds_in_stage = (
            WORK_SECONDS - self.seconds
            if self.seconds < WORK_SECONDS
            else BREAK_SECONDS - (self.seconds - WORK_SECONDS)
        )
        self.circle_fg.end_percentage = self.seconds / TOTAL_CYCLE_SECONDS
        self.circle_fg.start_percentage = max(
            0, 1 - (TOTAL_CYCLE_SECONDS - self.seconds) / RESET_SECONDS
        )


class TimerApp(App):
    def build(self):
        app = TimerCanvas()
        self.title = "Ouroboros Timer"
        Clock.schedule_interval(app.update, 1 / FPS)
        Window.size = (300, 450)
        return app


if __name__ == "__main__":
    TimerApp().run()
