# -*- coding: utf-8 -*-
from typing import Dict

from common.vector import Vector
from common.stats import RunningStats, Stats
from config import SKIP_FIRST_LINE


class EDDM:
    def __init__(self, warning_threshold=0.95, error_threshold=0.75):
        self.trained = {}
        self.means: Dict[str, Vector] = {}
        self.error_distance_stats = RunningStats()
        self.maximum_stats = Stats()
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
                if sum(self.trained.values()) < number_to_train:
                    self.train(new_vector)
                    last_error = counter
                    continue

                predicted_class = self.predict_class(new_vector)
                if predicted_class != new_vector.cls:
                    self.error_distance_stats.push(counter-last_error)
                    if self.error_distance_stats.value > self.maximum_stats.value:
                        self.maximum_stats.cache_stats(self.error_distance_stats)

                    last_error = counter  # mas tu chybu

                    if self.maximum_stats.value and self.error_distance_stats.value / self.maximum_stats.value < self.warning_threshold:
                        warning_counter += 1
                    else:
                        warning_counter = 0

                    if self.maximum_stats.value and self.error_distance_stats.value / self.maximum_stats.value < self.error_threshold:
                        error_counter += 1
                    else:
                        error_counter = 0

                if error_counter > 30:
                    print("Drift found")
                    error_counter = warning_counter = counter = last_error = 0
                    self.reset()
                    continue

                self.train(new_vector)

    def reset(self):
        self.error_distance_stats.reset()
        self.maximum_stats.reset()
        self.means.clear()
        self.trained.clear()

    def train(self, new_vector: Vector):
        if not self.means.get(new_vector.cls):
            self.trained[new_vector.cls] = 0
            self.means[new_vector.cls] = Vector(["0"] * len(new_vector.data) + [new_vector.cls])

        for i in range(len(new_vector.data)):
            self.means[new_vector.cls][i] = (self.means[new_vector.cls][i]*self.trained[new_vector.cls] + new_vector[i])/(self.trained[new_vector.cls] + 1)
        self.trained[new_vector.cls] += 1

    def predict_class(self, new_vector):
        found_class = None
        shortest_distance = float("inf")

        for cls, mean in self.means.items():
            distance = mean.distance(new_vector)
            if distance < shortest_distance:
                shortest_distance = distance
                found_class = cls

        return found_class
