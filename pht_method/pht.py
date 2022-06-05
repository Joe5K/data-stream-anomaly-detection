# -*- coding: utf-8 -*-
import math
from typing import List

from common.common import get_cur_time_str
from common.running_stats import RunningVectorStatistics
from common.vector import Vector
from config import SKIP_FIRST_LINE
from pht_method.weighted_stats import WeightedStats
from window_method.window import Window


class PageHinkley:
    def __init__(self, train_instances=100, threshold=50, alpha=0.99, delta=0.005):
        self.stats = WeightedStats(alpha, delta)
        self.train_instances = train_instances
        self.threshold = threshold

    def analyze(self, data: List[Vector]):
        counter = 0
        for vector in data:
            counter += 1
            self.stats.push(vector)
            if self.stats.count < self.train_instances:
                continue

            for distance_vector in self.stats.weighted_deviation.values():
                if sum(distance_vector) > self.threshold:
                    print(f"Drift occured after {counter} processed instances, time {get_cur_time_str()}")
                    return
                    counter = 0

    def reset(self):
        self.stats.reset()
