from typing import Dict

from common.running_stats import RunningVectorStatistics
from common.vector import Vector


class PHTStats(RunningVectorStatistics):
    # Class for running statistics used by PHT method.
    def __init__(self, alpha=0.999):
        # The constructor.
        super().__init__()
        self.weighted_sum_of_deviations: Dict[str, Vector] = {}
        self.alpha = alpha

    def reset(self):
        # Reset statistics after drift occurred.
        self.__init__(self.alpha)

    def push(self, vector: Vector, count=True) -> None:
        # Load new vector to statistics.
        super().push(vector)
        if not count:
            return

        if not self.weighted_sum_of_deviations.get(vector.cls):
            self.weighted_sum_of_deviations[vector.cls] = Vector([0] * len(vector))
            return

        for i in range(len(vector)):
            self.weighted_sum_of_deviations[vector.cls][i] = (
                    self.alpha * self.weighted_sum_of_deviations[vector.cls][i] + (
                        vector[i] - self.mean[vector.cls][i] - self.standard_deviation[vector.cls][i] / 2)
            )
