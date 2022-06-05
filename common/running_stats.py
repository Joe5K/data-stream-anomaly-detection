# -*- coding: utf-8 -*-
import math
from copy import deepcopy
from typing import Dict, List

from common.vector import Vector


class RunningVectorStatistics:
    def __init__(self):
        self._counter: Dict[str, int] = {}
        #._mean: Dict[str, Vector] = {}
        #self._variance_counter: Dict[str, Vector] = {}

        self.sum_: Dict[str, Vector] = {}
        self.sum_sqd: Dict[str, Vector] = {}

    @property
    def count(self):
        return sum(self._counter.values())

    def get_cls_count(self, cls: str):
        return self._counter[cls]

    @property
    def mean(self):
        out = {}

        for cls, sum_ in self.sum_.items():
            out[cls] = Vector([num / self._counter[cls] for num in sum_])

        return out

    @property
    def variance(self):
        out = {}

        for cls, sum_sqd in self.sum_sqd.items():
            mean = self.mean[cls]
            out[cls] = Vector([(sqd_num / self._counter[cls]) - mean_num**2 for sqd_num, mean_num in zip(sum_sqd, mean)])

        return out



    @property
    def standard_deviation(self) -> Dict[str, Vector]:
        out = {}

        for cls, variance in self.variance.items():
            out[cls] = Vector([str(math.sqrt(i)) for i in variance])

        return out

    @property
    def classes(self) -> List[str]:
        return list(self.mean.keys())

    '''
    @property
    def _variance(self) -> Dict[str, Vector]:
        out = {}

        for cls, S in self._variance_counter.items():
            out[cls] = Vector([(num / (self._counter[cls] - 1)) if self._counter[cls] > 1 else 0 for num in S])

        return out
    def is_vector_anomalous(self, vector: Vector, epsilon: float):
        mean = self._mean[vector.cls]
        variance = self.variance[vector.cls]

        product = 1
        for x, u, o2 in zip(vector, mean, variance):
            if o2 == 0:
                continue
            product *= (1 / (math.sqrt(2 * math.pi) * math.sqrt(o2))) * math.exp(-((x - u) ** 2) / (2 * o2))

        return product < epsilon
        '''

    def reset(self):
        self.__init__()

    def push(self, vector: Vector) -> None:
        if not self.mean.get(vector.cls):
            #self._mean[vector.cls] = deepcopy(vector)
            #self._variance_counter[vector.cls] = Vector([0] * len(vector))
            self._counter[vector.cls] = 1

            self.sum_[vector.cls] = deepcopy(vector)
            self.sum_sqd[vector.cls] = deepcopy(vector)
            for i in range(len(self.sum_sqd[vector.cls])):
                self.sum_sqd[vector.cls][i] = self.sum_sqd[vector.cls][i] ** 2
            return

        self._counter[vector.cls] += 1
        #old_mean = self._mean[vector.cls]
        #old_s = self._variance_counter[vector.cls]

        for i in range(len(vector)):
            #self._mean[vector.cls][i] = old_mean[i] + (vector[i] - old_mean[i]) / self._counter[vector.cls]
            #self._variance_counter[vector.cls][i] = old_s[i] + (vector[i] - old_mean[i]) * (vector[i] - self._mean[vector.cls][i])

            self.sum_[vector.cls][i] += vector[i]
            self.sum_sqd[vector.cls][i] += (vector[i] ** 2)

    def remove(self, vector: Vector) -> None:
        #old_mean = self._mean[vector.cls]
        #old_s = self._variance_counter[vector.cls]
        self._counter[vector.cls] -= 1

        for i in range(len(vector)):
            #self._mean[vector.cls][i] = old_mean[i] - (vector[i] - old_mean[i]) / self._counter[vector.cls]
            #self._variance_counter[vector.cls][i] = max(0., old_s[i] - (vector[i] - old_mean[i]) * (vector[i] - self._mean[vector.cls][i]))

            self.sum_[vector.cls][i] -= vector[i]
            self.sum_sqd[vector.cls][i] -= (vector[i] ** 2)

    def __repr__(self):
        return str(self.mean)

    def __getitem__(self, index) -> Vector:
        return self.mean[index]
