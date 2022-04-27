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

    @property
    def value(self):
        return self.mean + 2*self.standard_deviation

    def __repr__(self):
        return f"Mean:{self.mean}, standard deviation: {self.standard_deviation}"


class RunningStats(Stats):
    def __init__(self):
        super().__init__()
        self.n = 0
        self.old_M = self.new_M = 0
        self.old_S = self.new_S = 0

    def reset(self):
        self.__init__()

    def push(self, x):
        self.n += 1

        if self.n == 1:
            self.old_M = self.new_M = x
            self.old_S = 0
            return

        self.new_M = self.old_M + (x - self.old_M)/self.n
        self.new_S = self.old_S + (x - self.old_M)*(x - self.new_M)

        self.old_M = self.new_M
        self.old_S = self.new_S

    @property
    def mean(self):
        return self.new_M

    @property
    def variance(self):
        return self.new_S/(self.n - 1) if self.n > 1 else 0
