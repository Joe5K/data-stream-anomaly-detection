# -*- coding: utf-8 -*-
import math
from datetime import datetime
from typing import List

from common.running_stats import RunningVectorStatistics
from common.vector import Vector
from config import SKIP_FIRST_LINE
from pht_method.pht_stats import PHTStats
from window_method.window import Window


class PageHinkley:
    # Class representing Page-Hinkley Test.
    def __init__(self, train_instances=100, threshold=50, alpha=0.99):
        self.stats = PHTStats(alpha)
        self.train_instances = train_instances
        self.threshold = threshold

    def analyze(self, data: List[Vector]):
        # Process list of vectors.
        start = datetime.now()
        counter = 0
        for vector in data:
            counter += 1
            if self.stats.count < self.train_instances:
                self.stats.push(vector, count=False)
                continue

            self.stats.push(vector)

            for distance_vector in self.stats.weighted_sum_of_deviations.values():
                if abs(sum(distance_vector)) > self.threshold:
                    print(f"Drift occured after {counter} processed instances, took {(datetime.now()-start).total_seconds()} seconds")
                    counter = 0
                    self.reset()
        print(f"Processing of stream took {(datetime.now() - start).total_seconds()} seconds")

    def reset(self):
        # Reset method after drift occurred.
        self.stats.reset()
