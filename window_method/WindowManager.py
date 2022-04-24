# -*- coding: utf-8 -*-
from math import sqrt
from typing import List
from datetime import datetime
from window_method.Vector import Vector
from config import SKIP_FIRST_LINE
from window_method.Window import Window

import logging


class WindowManager:
    def __init__(self, windows_number: int, window_size: int, drift_threshold: float, step: int):
        self.windows: List[Window] = []
        self.windows_number = windows_number
        self.window_size = window_size
        self.drift_threshold = drift_threshold
        self.step = step
        self.counter = 0

    def init_windows(self):
        for i in range(self.windows_number):
            window = Window(self.window_size)
            self.windows.append(window)

    def compare_windows_means(self, first: int, second: int):
        first_window = self.windows[first]
        second_window = self.windows[second]

        sum = 0
        for cls in {*first_window.classes, *second_window.classes}:
            for i, j in zip(first_window.mean[cls], second_window.mean[cls]):
                sum += (i - j) ** 2
        return sqrt(sum)

    def find_drifts(self):
        for count, window in enumerate(self.windows[::-1]):
            index = len(self.windows) - 1 - count
            if index > 0:
                difference = self.compare_windows_means(index, index - 1)
                if difference > self.drift_threshold:
                    return difference
        return None

    def load_line(self, line):
        self.counter += 1
        new_vector = Vector.generate_vector(line)

        if not self.is_initialized:
            for window in self.windows:
                if not window.is_loaded:
                    window.load_vector(new_vector)
                    return

        for count, window in enumerate(self.windows[::-1]):
            new_vector = window.load_vector(new_vector)
        logging.info("Removing old data from stream", new_vector)

    def analyze(self, filename: str):
        print(f"Finding drifts by windows method, size of the window is {self.window_size}, the threshold is {self.drift_threshold}")
        with open(filename, "r") as input_stream:
            if SKIP_FIRST_LINE:
                input_stream.readline()
            self.init_windows()
            for line in input_stream.readlines():
                self.load_line(line)
                if self.is_initialized and self.counter % self.step == 0 and self.find_drifts():
                    print(f"Found drift at row {self.counter}, time {datetime.now().strftime('%H:%M:%S.%f')}")
                    self.clear_data()
        print("Data stream ended")

    def clear_data(self):
        for window in self.windows:
            window.data.clear()

    @property
    def is_initialized(self):
        for window in self.windows:
            if not window.is_loaded:
                return False
        return True
