from typing import List, Tuple

from config import SEPARATOR, WINDOW_SIZE
from app.Vector import Vector


class Window:
    def __init__(self):
        self.data: List[Vector] = []

    def load_line(self, line: str) -> None:
        if self.is_loaded:
            self.data.pop(0)
        data = line.replace("\n", "").split(SEPARATOR)
        self.data.append(Vector(data))

    @property
    def classes(self) -> List[str]:
        classes = []
        for i in self.data:
            if i.cls not in classes:
                classes.append(i.cls)
        return classes

    @property
    def classed_data(self):
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

        for class_name, class_data in self.classed_data.items():
            sum_vector = [0] * len(self.data[0])

            for vector in class_data:
                for index, value in enumerate(vector):
                    sum_vector[index] += value
            means[class_name] = tuple(i/len(class_data) for i in sum_vector)
        return means

    @property
    def variance(self) -> dict[str, tuple[float]]:
        variances = {}

        for class_name, class_data in self.classed_data.items():
            sum_vector = [0] * len(self.data[0])

            for vector in class_data:
                for index, value in enumerate(vector):
                    sum_vector[index] += (value - self.mean[class_name][index]) ** 2
            variances[class_name] = tuple(i/len(class_data) for i in sum_vector)
        return variances

    def __repr__(self) -> str:
        return str(self.mean)
