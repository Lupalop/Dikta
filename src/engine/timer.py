from engine.event_handler import EventHandler

import pygame
import time

class TimerManager():
    timers = []
    @classmethod
    def update(cls, game, events):
        for timer in cls.timers:
            timer.update(game.clock)
    @classmethod
    def add(cls, timer):
        cls.timers.append(timer)
    @classmethod
    def remove(cls, timer):
        cls.timers.remove(timer)

class Timer():
    def __init__(self, interval = None, enabled = False, auto_reset = False):
        if interval:
            self.interval = interval
        else:
            self.interval = 100.0
        self.time_elapsed = 0
        self.enabled = enabled
        self.removed = False
        self.auto_reset = auto_reset
        self.elapsed = EventHandler()
        self.tick = EventHandler()
        TimerManager.add(self)

    def __del__(self):
        self.close()

    def start(self):
        self.enabled = True

    def stop(self):
        self.enabled = False

    def reset(self, stop = False):
        if stop:
            self.stop()
        self.time_elapsed = 0

    def close(self):
        if not self.removed:
            TimerManager.remove(self)
            self.removed = True

    def on_elapsed(self):
        self.elapsed(self)

    def on_tick(self):
        self.tick(self)

    def update(self, clock):
        if not self.enabled:
            return

        self.time_elapsed += clock.get_time()

        if self.time_elapsed >= self.interval:
            self.on_elapsed()
            if self.auto_reset:
                self.reset()
            else:
                self.stop()
        else:
            self.on_tick()

    def get_remaining(self, in_seconds = False):
        remaining = (self.interval - self.time_elapsed)
        if in_seconds:
            return remaining / 1000
        return remaining

    def get_elapsed(self, in_seconds = False):
        if in_seconds:
            return self.time_elapsed / 1000
        return self.time_elapsed
