import math
from typing import List, Optional

from copy import deepcopy
from common.Vector import Vector


class Window:
    def __init__(self, window_size):
        self.data: List[Vector] = []
        self.window_size = window_size

    def load_vector(self, input_vector: Vector) -> Optional[Vector]:
        popping_vector = None
        if self.is_loaded:
            popping_vector = self.data.pop(0)
        self.data.append(input_vector)
        return popping_vector

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
        assert len(self.data) <= self.window_size

        return len(self.data) == self.window_size

    @property
    def means(self) -> dict[str, Vector]:
        means = {}

        for class_name, class_data in self.classified_data.items():
            sum_vector = [0] * len(class_data[0])

            for vector in class_data:
                for index, value in enumerate(vector):
                    sum_vector[index] += value
            means[class_name] = Vector(list(i/len(class_data) for i in sum_vector)+[class_name])
        return means

    @property
    def variances(self) -> dict[str, Vector]:
        variances = {}
        means = deepcopy(self.means)

        for class_name, class_data in self.classified_data.items():
            sum_vector = [0] * len(class_data[0])

            for vector in class_data:
                for index, value in enumerate(vector):
                    sum_vector[index] += (value - means[class_name][index]) ** 2
            variances[class_name] = Vector(list(i/len(class_data) for i in sum_vector)+[class_name])
        return variances
    
    @property
    def standard_deviations(self) -> dict[str, Vector]:
        deviations = {}

        for class_name, variation_vector in self.variances.items():
            cached_data = []
            for data in variation_vector:
                cached_data.append(str(math.sqrt(data)))
            deviations[class_name] = Vector(cached_data + [class_name])
        return deviations

    def __repr__(self) -> str:
        return str(self.means)
