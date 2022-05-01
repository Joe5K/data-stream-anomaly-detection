# -*- coding: utf-8 -*-
import math

from common.common import get_cur_time_str
from common.vector import Vector
from config import SKIP_FIRST_LINE
from window_method.window import Window


class PageHinkley:
    def __init__(self, window_size: int, threshold=0.8):
        self.static_window = Window(window_size)
        self.dynamic_window = Window(window_size)
        self.threshold = threshold

    def analyze(self, filename: str):
        counter = error_counter = 0
        with open(filename, "r") as reader:
            if SKIP_FIRST_LINE:
                reader.readline()
            for line in reader.readlines():
                counter += 1
                new_vector = Vector.generate_vector(line)
                if not self.static_window.is_loaded:
                    self.static_window.load_vector(new_vector)
                    self.dynamic_window.load_vector(new_vector)
                    continue

                self.dynamic_window.load_vector(new_vector)

                if self.static_window.running_stats.mean[new_vector.cls].distance(self.dynamic_window.running_stats.mean[new_vector.cls]) > self.threshold:
                    print(f"Drift occured after {counter} processed instances, time {get_cur_time_str()}")
                    counter = 0
                    self.static_window.reset()
                    self.dynamic_window.reset()
