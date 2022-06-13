# -*- coding: utf-8 -*-
import math
from copy import deepcopy
from typing import Dict, List

from common.vector import Vector


class RunningVectorStatistics:
    # Helping class for counting mean and variance, able to push and remove vectors.

    def __init__(self):
        # The constructor.
        self._counter: Dict[str, int] = {}
        self.sum_: Dict[str, Vector] = {}
        self.sum_sqd: Dict[str, Vector] = {}

    @property
    def count(self):
        # Number of loaded vectors.
        return sum(self._counter.values())

    def get_cls_count(self, cls: str):
        # Number of loaded vectors by their classification
        return self._counter[cls]

    @property
    def mean(self):
        # Classifications and their means.
        out = {}

        for cls, sum_ in self.sum_.items():
            out[cls] = Vector([num / self._counter[cls] for num in sum_])

        return out

    @property
    def variance(self):
        # Classifications and their variances.
        out = {}

        for cls, sum_sqd in self.sum_sqd.items():
            mean = self.mean[cls]
            out[cls] = Vector([(sqd_num / self._counter[cls]) - mean_num**2 for sqd_num, mean_num in zip(sum_sqd, mean)])

        return out

    @property
    def standard_deviation(self) -> Dict[str, Vector]:
        # Classifications and their standard deviations.
        out = {}

        for cls, variance in self.variance.items():
            out[cls] = Vector([str(math.sqrt(i)) for i in variance])

        return out

    @property
    def classes(self) -> List[str]:
        # List of all classifications loaded in statistics.
        return list(self.mean.keys())

    def reset(self):
        # Reset statistics, remove all items.
        self.__init__()

    def push(self, vector: Vector) -> None:
        # Load new vector to statistics.
        if not self.mean.get(vector.cls):
            self._counter[vector.cls] = 1

            self.sum_[vector.cls] = deepcopy(vector)
            self.sum_sqd[vector.cls] = deepcopy(vector)
            for i in range(len(self.sum_sqd[vector.cls])):
                self.sum_sqd[vector.cls][i] = self.sum_sqd[vector.cls][i] ** 2
            return

        self._counter[vector.cls] += 1

        for i in range(len(vector)):
            self.sum_[vector.cls][i] += vector[i]
            self.sum_sqd[vector.cls][i] += (vector[i] ** 2)

    def remove(self, vector: Vector) -> None:
        # Remove vector from statistics.
        self._counter[vector.cls] -= 1

        for i in range(len(vector)):
            self.sum_[vector.cls][i] -= vector[i]
            self.sum_sqd[vector.cls][i] -= (vector[i] ** 2)

    def __repr__(self):
        # Convert statistics to string.
        return str(self.mean)
