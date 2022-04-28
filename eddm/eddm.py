# -*- coding: utf-8 -*-
from typing import Tuple

from common.running_stats import RunningVectorStatistics
from common.vector import Vector
from eddm.stats import RunningStats, Stats
from config import SKIP_FIRST_LINE


class EDDMData:
    def __init__(self):
        self.running_mean = RunningVectorStatistics()
        self.error_distance_stats = RunningStats()
        self.maximum_stats = Stats()


class EDDM:
    def __init__(self, warning_threshold=0.95, error_threshold=0.75):
        self.data = EDDMData()
        # self.temporary_data = EDDMData()  # TODO keep warning data here
        self.warning_threshold = warning_threshold
        self.error_threshold = error_threshold

    def analyze(self, number_to_train: int, filename: str):
        with open(filename, "r") as reader:
            if SKIP_FIRST_LINE:
                reader.readline()
            error_counter = warning_counter = counter = 0
            for line in reader.readlines():
                counter += 1
                new_vector = Vector.generate_vector(line)
                if self.data.running_mean.count < number_to_train:
                    self.train(new_vector)
                    last_error = counter
                    continue

                predicted_class = self.predict_class(new_vector)
                if predicted_class != new_vector.cls:
                    self.process_error(number_of_processed_without_error=counter-last_error)
                    last_error = counter

                    warning, error = self.get_warning_and_error()

                    if warning:
                        warning_counter += 1
                    else:
                        warning_counter = 0

                    if error:
                        error_counter += 1
                    else:
                        error_counter = 0

                if error_counter > 30:
                    print("Drift found")
                    error_counter = warning_counter = counter = last_error = 0
                    self.reset()
                    continue

                self.train(new_vector)

    def process_error(self, number_of_processed_without_error):
        self.data.error_distance_stats.push(number_of_processed_without_error)

        if self.data.error_distance_stats > self.data.maximum_stats:
            self.data.maximum_stats.cache_stats(self.data.error_distance_stats)

    def get_warning_and_error(self) -> Tuple[bool, bool]:
        if not self.data.maximum_stats:
            return False, False
        result = self.data.error_distance_stats / self.data.maximum_stats
        return result < self.warning_threshold, result < self.error_threshold

    def reset(self):
        self.data.error_distance_stats.reset()
        self.data.maximum_stats.reset()
        self.data.running_mean.reset()

    def train(self, new_vector: Vector):
        self.data.running_mean.push(new_vector)

    def predict_class(self, new_vector):
        found_class = None
        shortest_distance = float("inf")

        for cls, mean in self.data.running_mean.mean.items():
            distance = mean.distance(new_vector)
            if distance < shortest_distance:
                shortest_distance = distance
                found_class = cls

        return found_class
