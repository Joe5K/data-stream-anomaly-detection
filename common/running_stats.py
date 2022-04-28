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
            out[cls] = Vector([(num / (self._counter[cls] - 1)) if self._counter[cls] > 1 else 0 for num in S] + [cls])

        return out

    @property
    def standard_deviation(self) -> Dict[str, Vector]:
        out = {}

        for cls, variance in self.variance.items():
            out[cls] = Vector([str(math.sqrt(i)) for i in variance]+[cls])

        return out

    def reset(self):
        self.__init__()

    def push(self, new_vector: Vector) -> None:
        if not self.mean.get(new_vector.cls):
            self.mean[new_vector.cls] = deepcopy(new_vector)
            self._variance_counter[new_vector.cls] = Vector([0] * len(new_vector) + [new_vector.cls])
            self._counter[new_vector.cls] = 1
            return

        self._counter[new_vector.cls] += 1
        old_mean = self.mean[new_vector.cls]
        old_s = self._variance_counter[new_vector.cls]

        for i in range(len(new_vector)):
            self.mean[new_vector.cls][i] = old_mean[i] + (new_vector[i] - old_mean[i]) / self._counter[new_vector.cls]
            self._variance_counter[new_vector.cls][i] = old_s[i] + (new_vector[i] - old_mean[i]) * (new_vector[i] - self.mean[new_vector.cls][i])

    def remove(self, old_vector: Vector) -> None:
        old_mean = self.mean[old_vector.cls]
        old_s = self._variance_counter[old_vector.cls]
        self._counter[old_vector.cls] -= 1

        for i in range(len(old_vector)):
            self.mean[old_vector.cls][i] = old_mean[i] - (old_vector[i] - old_mean[i]) / self._counter[old_vector.cls]
            self._variance_counter[old_vector.cls][i] = old_s[i] - (old_vector[i] - old_mean[i]) * (old_vector[i] - self.mean[old_vector.cls][i])

    def __repr__(self):
        return str(self.mean)

    def __getitem__(self, index) -> Vector:
        return self.mean[index]
