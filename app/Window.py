from typing import List, Tuple, Optional

from config import SEPARATOR, WINDOW_SIZE
from app.Vector import Vector


class Window:
    def __init__(self):
        self.data: List[Vector] = []

    def load_vector(self, input_vector: Vector) -> Optional[Vector]:
        popping_vector = None
        if self.is_loaded:
            popping_vector = self.data.pop(0)
        self.data.append(input_vector)
        return popping_vector

    def compare_vector(self, new_vector: Vector) -> float:
        variation = 0
        for i, j in zip(new_vector, self.mean.get(new_vector.cls)):
            variation += (i - j)**2
        return variation

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
        assert len(self.data) <= WINDOW_SIZE

        return len(self.data) == WINDOW_SIZE

    @property
    def mean(self) -> dict[str, tuple[float]]:
        means = {}

        for class_name, class_data in self.classified_data.items():
            sum_vector = [0] * len(class_data[0])

            for vector in class_data:
                for index, value in enumerate(vector):
                    sum_vector[index] += value
            means[class_name] = tuple(i/len(class_data) for i in sum_vector)
        return means

    @property
    def variance(self) -> dict[str, tuple[float]]:
        variances = {}

        for class_name, class_data in self.classified_data.items():
            sum_vector = [0] * len(class_data[0])

            for vector in class_data:
                for index, value in enumerate(vector):
                    sum_vector[index] += (value - self.mean[class_name][index]) ** 2
            variances[class_name] = tuple(i/len(class_data) for i in sum_vector)
        return variances

    def __repr__(self) -> str:
        return str(self.mean)
