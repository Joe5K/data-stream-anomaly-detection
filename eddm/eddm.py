# -*- coding: utf-8 -*-
from typing import Tuple

from common.common import get_cur_time_str
from common.naive_bayers import naive_bayers_distance
from common.running_stats import RunningVectorStatistics
from common.vector import Vector
from eddm.eddmstats import RunningEDDMStats, EDDMStats
from config import SKIP_FIRST_LINE


class EDDM:
    def __init__(self, train_instances=100, error_threshold=0.75):
        self.running_mean = RunningVectorStatistics()
        self.misprediction_distance_stats = RunningEDDMStats()
        self.maximum_misprediction_distance = EDDMStats()
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
                if self.running_mean.count < self.train_instances:
                    self.train(new_vector)
                    last_error = counter
                    continue

                predicted_class = self.predict_class(new_vector)
                if predicted_class != new_vector.cls:
                    self.process_misprediction(number_of_processed_without_error=counter - last_error)
                    last_error = counter

                    if self.is_error():
                        error_counter = error_counter + 1

                if error_counter > 30:
                    print(f"Drift found after {counter} processed instances, time {get_cur_time_str()}")
                    error_counter = counter = last_error = 0
                    self.reset()
                    continue

    def process_misprediction(self, number_of_processed_without_error):
        self.misprediction_distance_stats.push(number_of_processed_without_error)

        if self.misprediction_distance_stats > self.maximum_misprediction_distance:
            self.maximum_misprediction_distance.cache_stats(self.misprediction_distance_stats)

    def is_error(self) -> bool:
        if not self.maximum_misprediction_distance:
            return False
        result = self.misprediction_distance_stats / self.maximum_misprediction_distance
        return result < self.error_threshold

    def reset(self):
        self.misprediction_distance_stats.reset()
        self.maximum_misprediction_distance.reset()
        self.running_mean.reset()

    def train(self, new_vector: Vector):
        self.running_mean.push(new_vector)

    def predict_class(self, new_vector):
        found_class = None
        highest_probability = 0

        for cls in self.running_mean.classes:
            mean = self.running_mean.mean[cls]
            variance = self.running_mean.variance[cls]
            cls_count_division = self.running_mean.get_cls_count(cls)/self.running_mean.count
            probability = naive_bayers_distance(new_vector, mean, variance, cls_count_division)
            if probability > highest_probability:
                highest_probability = probability
                found_class = cls

        return found_class
