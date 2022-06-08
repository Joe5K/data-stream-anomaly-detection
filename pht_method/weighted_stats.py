from typing import Dict

from common.running_stats import RunningVectorStatistics
from common.vector import Vector


class WeightedStats(RunningVectorStatistics):
    def __init__(self, alpha=0.99):
        super().__init__()
        self.weighted_deviation: Dict[str, Vector] = {}
        self.alpha = alpha

    def reset(self):
        self.__init__(self.alpha)

    def push(self, vector: Vector, count=True) -> None:
        super().push(vector)
        if not count:
            return

        if not self.weighted_deviation.get(vector.cls):
            self.weighted_deviation[vector.cls] = Vector([0] * len(vector))
            return

        for i in range(len(vector)):
            self.weighted_deviation[vector.cls][i] = (
                    self.alpha * self.weighted_deviation[vector.cls][i] + (
                        vector[i] - self.mean[vector.cls][i] - self.standard_deviation[vector.cls][i] / 2)
            )
