# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Tuple, List

from common.naive_bayers import naive_bayers_distance
from common.running_stats import RunningVectorStatistics
from common.vector import Vector
from eddm.eddm_stats import RunningEDDMStats, EDDMStats
from config import SKIP_FIRST_LINE


class EDDM:
    # Class representing Early Drift Detection Method.

    def __init__(self, train_instances=100, error_threshold=0.75):
        # The constructor.
        self.running_mean = RunningVectorStatistics()
        self.misprediction_distance_stats = RunningEDDMStats()
        self.maximum_misprediction_distance = EDDMStats()
        self.train_instances = train_instances
        self.error_threshold = error_threshold

    def analyze(self, data: List[Vector]):
        # Process list of vectors.
        start = datetime.now()
        counter = 0
        for new_vector in data:
            counter += 1
            if self.running_mean.count < self.train_instances:
                self.train(new_vector)
                last_error = counter
                continue

            predicted_class = self.predict_class(new_vector)
            if predicted_class != new_vector.cls:
                distance = counter - last_error
                self.process_misprediction(number_of_processed_without_error=distance)
                last_error = counter

                if self.is_error():
                    if counter > self.train_instances * 2:
                        print(
                            f"Drift found after {counter} processed instances, took {(datetime.now() - start).total_seconds()} seconds")
                    counter = last_error = 0
                    self.reset()
                    continue

        print(f"Processing of stream took {(datetime.now() - start).total_seconds()} seconds")

    def process_misprediction(self, number_of_processed_without_error):
        # Process wrong prediction.
        self.misprediction_distance_stats.push(number_of_processed_without_error)

        if self.misprediction_distance_stats > self.maximum_misprediction_distance:
            self.maximum_misprediction_distance.cache_stats(self.misprediction_distance_stats)

    def is_error(self) -> bool:
        # Check ratio of misprediction values and determine, whether drift happened.
        if not self.maximum_misprediction_distance:
            return False
        result = self.misprediction_distance_stats / self.maximum_misprediction_distance
        return result < self.error_threshold

    def reset(self):
        # Reset method after drift occurred.
        self.misprediction_distance_stats.reset()
        self.maximum_misprediction_distance.reset()
        self.running_mean.reset()

    def train(self, new_vector: Vector):
        # Train the classifier with new data
        self.running_mean.push(new_vector)

    def predict_class(self, new_vector):
        # Predict classification for new data
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
