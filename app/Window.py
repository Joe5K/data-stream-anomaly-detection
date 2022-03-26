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
    def is_loaded(self) -> bool:
        return len(self.data) >= WINDOW_SIZE

    @property
    def mean(self) -> dict[str, tuple[float]]:
        classes_sums: dict[str, list[float]] = {}
        classes_usage: dict[str, int] = {}
        for vector in self.data:

            vector_class = vector.cls
            if classes_sums.get(vector_class):
                sum_vector = classes_sums[vector_class]
                classes_usage[vector_class] += 1
            else:
                classes_sums[vector_class] = sum_vector = [0] * len(self.data[0])
                classes_usage[vector_class] = 1

            for index, data in enumerate(vector):
                sum_vector[index] += data

        mean_out: dict[str, tuple[float]] = {}

        for vector_class, sum_vector in classes_sums.items():
            mean_out[vector_class] = tuple([i / classes_usage[vector_class] for i in sum_vector])

        return mean_out

    @property
    def variance(self) -> dict[str, tuple[float]]:
        classes_sums: dict[str, list[float]] = {}
        classes_usage: dict[str, int] = {}
        for vector in self.data:

            vector_class = vector.cls
            if classes_sums.get(vector_class):
                sum_vector = classes_sums[vector_class]
                classes_usage[vector_class] += 1
            else:
                classes_sums[vector_class] = sum_vector = [0] * len(self.data[0])
                classes_usage[vector_class] = 1

            for index, data in enumerate(vector):
                sum_vector[index] += (data - self.mean[vector_class][index]) ** 2

        variance_out: dict[str, tuple[float]] = {}

        for vector_class, sum_vector in classes_sums.items():
            variance_out[vector_class] = tuple([i / classes_usage[vector_class] for i in sum_vector])

        return variance_out

    def __repr__(self) -> str:
        return str(self.mean)
