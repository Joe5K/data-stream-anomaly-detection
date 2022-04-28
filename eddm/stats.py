# -*- coding: utf-8 -*-
import math


class Stats:
    def __init__(self):
        self._cached_mean = 0
        self._cached_variance = 0

    def cache_stats(self, stats):
        self._cached_mean = stats.mean
        self._cached_variance = stats.variance

    def reset(self):
        self.__init__()

    @property
    def mean(self):
        return self._cached_mean

    @property
    def variance(self):
        return self._cached_variance

    @property
    def standard_deviation(self):
        return math.sqrt(self.variance)

    def __gt__(self, other):
        return float(self) > float(other)

    def __lt__(self, other):
        return not self > other

    def __truediv__(self, other):
        return float(self) / float(other)

    def __float__(self):
        return self.mean + 2*self.standard_deviation

    def __repr__(self):
        return f"Mean:{self.mean}, standard deviation: {self.standard_deviation}"


class RunningStats(Stats):
    def __init__(self):
        super().__init__()
        self.n = 0
        self.M = 0
        self.S = 0

    def reset(self):
        self.__init__()

    def push(self, x):
        self.n += 1

        if self.n == 1:
            self.M = x
            return

        old_m = self.M
        old_s = self.S

        self.M = old_m + (x - old_m)/self.n
        self.S = old_s + (x - old_m)*(x - self.M)

    @property
    def mean(self):
        return self.M

    @property
    def variance(self):
        return self.S/(self.n - 1) if self.n > 1 else 0
