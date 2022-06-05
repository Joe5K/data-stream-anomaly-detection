from typing import Dict

from common.running_stats import RunningVectorStatistics
from common.vector import Vector


class WeightedStats(RunningVectorStatistics):
    def __init__(self, alpha=0.99, delta=0.005):
        super().__init__()
        self.weighted_deviation: Dict[str, Vector] = {}
        self.alpha = alpha
        self.delta = delta

    def reset(self):
        self.__init__(self.alpha, self.delta)

    def push(self, vector: Vector) -> None:
        super().push(vector)
        if not self.weighted_deviation.get(vector.cls):
            self.weighted_deviation[vector.cls] = Vector([0] * len(vector))
            return

        for i in range(len(vector)):
            self.weighted_deviation[vector.cls][i] = (
                    self.alpha * self.weighted_deviation[vector.cls][i]
                    + abs(abs(vector[i] - self.mean[vector.cls][i]) - self.delta)
            )
