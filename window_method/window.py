# -*- coding: utf-8 -*-
import math
from copy import deepcopy
from typing import List, Optional, Dict

from common.vector import Vector
from common.running_stats import RunningVectorStatistics


class Window:
    def __init__(self, window_size):
        self.data: List[Vector] = []
        self.window_size = window_size
        self.running_stats = RunningVectorStatistics()

    def load_vector(self, input_vector: Vector) -> Optional[Vector]:
        popping_vector = None
        if self.is_loaded:
            popping_vector = self.data.pop(0)
            self.running_stats.remove(popping_vector)
        self.data.append(input_vector)
        self.running_stats.push(input_vector)
        return popping_vector

    def reset(self):
        self.running_stats.reset()
        self.data.clear()

    @property
    def current_data_len(self):
        return len(self.data)

    @property
    def classes(self) -> List[str]:
        return list({i.cls for i in self.data})

    @property
    def classified_data(self):
        classed_data = {i: [] for i in self.classes}
        for i in self.data:
            classed_data[i.cls].append(i.data)
        return classed_data

    @property
    def is_loaded(self) -> bool:
        assert self.current_data_len <= self.window_size

        return self.current_data_len == self.window_size

    def __repr__(self) -> str:
        return str(self.running_stats)
