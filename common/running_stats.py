# -*- coding: utf-8 -*-
import math
from copy import deepcopy
from typing import Dict

from common.vector import Vector


class RunningVectorStatistics:
    def __init__(self):
        self._counter: Dict[str, int] = {}
        self.mean: Dict[str, Vector] = {}
        self._variance_counter: Dict[str, Vector] = {}

    @property
    def count(self):
        return sum(self._counter.values())

    @property
    def variance(self) -> Dict[str, Vector]:
        out = {}

        for cls, S in self._variance_counter.items():
            out[cls] = Vector([(num / (self._counter[cls] - 1)) if self._counter[cls] > 1 else 0 for num in S])

        return out

    @property
    def standard_deviation(self) -> Dict[str, Vector]:
        out = {}

        for cls, variance in self.variance.items():
            out[cls] = Vector([str(math.sqrt(i)) for i in variance])

        return out

    '''def is_vector_anomalous(self, vector: Vector, epsilon: float):
        mean = self.mean[vector.cls]
        variance = self.variance[vector.cls]

        product = 1
        for x, u, o2 in zip(vector, mean, variance):
            if o2 == 0:
                continue
            product *= (1 / (math.sqrt(2 * math.pi) * math.sqrt(o2))) * math.exp(-((x - u) ** 2) / (2 * o2))

        return product < epsilon'''

    def reset(self):
        self.__init__()

    def push(self, vector: Vector) -> None:
        if not self.mean.get(vector.cls):
            self.mean[vector.cls] = deepcopy(vector)
            self._variance_counter[vector.cls] = Vector([0] * len(vector))
            self._counter[vector.cls] = 1
            return

        self._counter[vector.cls] += 1
        old_mean = self.mean[vector.cls]
        old_s = self._variance_counter[vector.cls]

        for i in range(len(vector)):
            self.mean[vector.cls][i] = old_mean[i] + (vector[i] - old_mean[i]) / self._counter[vector.cls]
            self._variance_counter[vector.cls][i] = old_s[i] + (vector[i] - old_mean[i]) * (vector[i] - self.mean[vector.cls][i])

    def remove(self, vector: Vector) -> None:
        old_mean = self.mean[vector.cls]
        old_s = self._variance_counter[vector.cls]
        self._counter[vector.cls] -= 1

        for i in range(len(vector)):
            self.mean[vector.cls][i] = old_mean[i] - (vector[i] - old_mean[i]) / self._counter[vector.cls]
            self._variance_counter[vector.cls][i] = max(0., old_s[i] - (vector[i] - old_mean[i]) * (vector[i] - self.mean[vector.cls][i]))

    def __repr__(self):
        return str(self.mean)

    def __getitem__(self, index) -> Vector:
        return self.mean[index]
