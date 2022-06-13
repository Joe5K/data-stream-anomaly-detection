# -*- coding: utf-8 -*-
import math


class EDDMStats:
    # Class for statistics used by EDDM method.
    def __init__(self):
        # The constructor.
        self._cached_mean = 0
        self._cached_variance = 0

    def cache_stats(self, stats):
        # Save stats values to cache.
        self._cached_mean = stats.mean
        self._cached_variance = stats.variance

    def reset(self):
        # Reset stats by deleting all saved values.
        self.__init__()

    @property
    def mean(self):
        # Get cached mean.
        return self._cached_mean

    @property
    def variance(self):
        # Get cached variance.
        return self._cached_variance

    @property
    def standard_deviation(self):
        # Get standard deviation mean.
        return math.sqrt(self.variance)

    def __gt__(self, other):
        # Compare two statistics values.
        return float(self) > float(other)

    def __lt__(self, other):
        # Compare two statistics values.
        return not self > other

    def __truediv__(self, other):
        # Divide two statistics values.
        return float(self) / float(other)

    def __float__(self):
        # Get statistics values.
        return self.mean + 2*self.standard_deviation

    def __bool__(self):
        # Check whether statistics are empty.
        return bool(float(self))

    def __repr__(self):
        # Get statistics string.
        return f"Mean:{self.mean}, standard deviation: {self.standard_deviation}"


class RunningEDDMStats(EDDMStats):
    # Running EDDM statistics.
    def __init__(self):
        # The constructor.
        super().__init__()
        self.n = 0
        self.M = 0
        self.S = 0

    def push(self, x):
        # Push new vector to running statistics.
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
        # Get running statistics mean.
        return self.M

    @property
    def variance(self):
        # Get running statistics variance.
        return self.S/(self.n - 1) if self.n > 1 else 0
