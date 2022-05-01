# -*- coding: utf-8 -*-
from common.common import get_cur_time_str
from common.vector import Vector
from config import SKIP_FIRST_LINE
from window_method.window import Window


class PageHinkley:
    def __init__(self, window_size: int, threshold=0.8):
        self.window = Window(window_size)
        self.threshold = threshold

    def analyze(self, number_to_train: int, filename: str):
        counter = error_counter = 0
        with open(filename, "r") as reader:
            if SKIP_FIRST_LINE:
                reader.readline()
            for line in reader.readlines():
                counter += 1
                new_vector = Vector.generate_vector(line)
                if self.window.current_data_len < number_to_train:
                    self.window.load_vector(new_vector)
                    continue

                if new_vector.distance(self.window.running_mean[new_vector.cls]) > self.threshold:
                    error_counter += 1
                else:
                    error_counter = 0

                if error_counter > 30:
                    print(f"Drift occured after {counter} processed instances, time {get_cur_time_str()}")
                    counter = error_counter = 0
                    self.window.reset()
