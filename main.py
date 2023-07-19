import time

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.widget import Widget


WORK_MINUTES = 25 / 10
BREAK_MINUTES = 5 / 10
TOTAL_CYCLE_MINUTES = WORK_MINUTES + BREAK_MINUTES

WORK_SECONDS = WORK_MINUTES * 60
BREAK_SECONDS = BREAK_MINUTES * 60
TOTAL_CYCLE_SECONDS = TOTAL_CYCLE_MINUTES * 60


class TimerBG(Widget):
    switch_angle = NumericProperty(WORK_SECONDS / TOTAL_CYCLE_SECONDS * 360)


class TimerCircle(Widget):
    percentage = NumericProperty(0)


class TimerCanvas(Widget):
    seconds = NumericProperty(0)
    remaining_seconds = NumericProperty(0)
    remaining_seconds_in_stage = NumericProperty(0)
    circle_fg = ObjectProperty(None)
    circle_size = NumericProperty(0)

    def update(self, dt):
        self.seconds = time.time() % TOTAL_CYCLE_SECONDS
        self.remaining_seconds = TOTAL_CYCLE_SECONDS - self.seconds
        self.remaining_seconds_in_stage = (
            WORK_SECONDS - self.seconds
            if self.seconds < WORK_SECONDS
            else BREAK_SECONDS - (self.seconds - WORK_SECONDS)
        )
        self.circle_fg.percentage = self.seconds / TOTAL_CYCLE_SECONDS


class TimerApp(App):
    def build(self):
        app = TimerCanvas()
        self.title = "Ouroboros Timer"
        Clock.schedule_interval(app.update, 1 / 60)
        return app


if __name__ == "__main__":
    TimerApp().run()
