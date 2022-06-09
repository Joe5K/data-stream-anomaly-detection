# -*- coding: utf-8 -*-
from math import sqrt
from typing import List
from datetime import datetime

from common.common import get_cur_time_str
from common.vector import Vector
from config import SKIP_FIRST_LINE
from window_method.window import Window

import logging


class WindowManager:
    def __init__(self, windows_number: int, window_size: int, drift_threshold: float, step: int):
        self.windows: List[Window] = []
        self.drift_threshold = drift_threshold**2
        self.step = step

        self.init_windows(windows_number, window_size)

    def init_windows(self, windows_number, window_size):
        for i in range(windows_number):
            window = Window(window_size)
            self.windows.append(window)

    def compare_windows_means(self, first_index: int, second_index: int):
        first_window = self.windows[first_index]
        second_window = self.windows[second_index]

        sum = 0
        for cls in {*first_window.classes, *second_window.classes}:
            for i, j in zip(first_window.running_stats[cls], second_window.running_stats[cls]):
                sum += (i - j) ** 2
        return sum

    def load_vector(self, new_vector: Vector):
        if not self.is_initialized:
            for window in self.windows:
                if not window.is_loaded:
                    window.load_vector(new_vector)
                    return

        for count, window in enumerate(self.windows[::-1]):
            new_vector = window.load_vector(new_vector)
            break
        logging.info("Removing old data from stream", new_vector)

    def analyze(self, data: List[Vector]):
        start = datetime.now()
        counter = 0
        for vector in data:
            counter += 1
            self.load_vector(vector)
            if self.is_initialized and counter % self.step == 0:
                difference = self.compare_windows_means(first_index=0, second_index=1)
                if difference > self.drift_threshold:
                    if counter > self.windows[0].window_size*2:
                        return counter
                        print(f"Drift found after {counter} instances, took {(datetime.now()-start).total_seconds()} seconds")
                    counter = 0
                    self.clear_data()
        #print(f"Processing of stream took {(datetime.now()-start).total_seconds()} seconds")

    def clear_data(self):
        for window in self.windows:
            window.data.clear()
            window.running_stats.reset()

    @property
    def is_initialized(self):
        for window in self.windows:
            if not window.is_loaded:
                return False
        return True
