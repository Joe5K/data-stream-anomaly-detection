# -*- coding: utf-8 -*-
import math
from typing import List, Union

from config import SEPARATOR


class Vector:
    def __init__(self, data: List[Union[str, float]], last_column_is_class=True):
        if last_column_is_class:
            self.data = list(float(i) for i in data[:-1])
            self.cls = data[-1]
        else:
            self.data = list(float(i) for i in data)
            self.cls = None

    @staticmethod
    def generate_vector(input_line):
        data = input_line.replace("\n", "").split(SEPARATOR)
        vector = Vector(data)
        return vector

    def distance(self, other_vector):
        sum = 0
        for i, j in zip(self, other_vector):
            sum += (i - j)**2
        return math.sqrt(sum)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index) -> float:
        if index < len(self):
            return self.data[index]

    def __setitem__(self, key, value):
        if key < len(self):
            self.data[key] = value

    def __iter__(self) -> iter:
        return iter(self.data)

    def __repr__(self) -> str:
        return f"class: {self.cls}; data: {str(self.data)}"
