# -*- coding: utf-8 -*-
from typing import Tuple

from common.common import get_cur_time_str
from common.running_stats import RunningVectorStatistics
from common.vector import Vector
from eddm.eddmstats import RunningEDDMStats, EDDMStats
from config import SKIP_FIRST_LINE


class EDDMData:
    def __init__(self):
        self.running_mean = RunningVectorStatistics()
        self.misprediction_distance_stats = RunningEDDMStats()
        self.maximum_misprediction_distance = EDDMStats()


class EDDM:
    def __init__(self, train_instances=100, error_threshold=0.75):
        self.data = EDDMData()
        self.train_instances = train_instances
        self.error_threshold = error_threshold

    def analyze(self, filename: str):
        with open(filename, "r") as reader:
            if SKIP_FIRST_LINE:
                reader.readline()
            error_counter = counter = 0
            for line in reader.readlines():
                counter += 1
                new_vector = Vector.generate_vector(line)
                if self.data.running_mean.count < self.train_instances:
                    self.train(new_vector)
                    last_error = counter
                    continue

                predicted_class = self.predict_class(new_vector)
                if predicted_class != new_vector.cls:
                    self.process_misprediction(number_of_processed_without_error=counter - last_error)
                    last_error = counter

                    error_counter = error_counter + 1 if self.is_error() else 0

                if error_counter > 30:
                    print(f"Drift found after {counter} processed instances, time {get_cur_time_str()}")
                    error_counter = counter = last_error = 0
                    self.reset()
                    continue

                self.train(new_vector)

    def process_misprediction(self, number_of_processed_without_error):
        self.data.misprediction_distance_stats.push(number_of_processed_without_error)

        if self.data.misprediction_distance_stats > self.data.maximum_misprediction_distance:
            self.data.maximum_misprediction_distance.cache_stats(self.data.misprediction_distance_stats)

    def is_error(self) -> bool:
        if not self.data.maximum_misprediction_distance:
            return False
        result = self.data.misprediction_distance_stats / self.data.maximum_misprediction_distance
        return result < self.error_threshold

    def reset(self):
        self.data.misprediction_distance_stats.reset()
        self.data.maximum_misprediction_distance.reset()
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
