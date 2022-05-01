# -*- coding: utf-8 -*-
import math
from typing import Union, Optional, Iterable

from config import SEPARATOR


class Vector:
    def __init__(self, data: Iterable[Union[str, float]], cls: Optional[str] = None):
        self.data = list(float(i) for i in data)
        if cls:
            self.cls = cls

    @staticmethod
    def generate_vector(input_line):
        data = input_line.replace("\n", "").split(SEPARATOR)
        vector = Vector(data=data[:-1], cls=data[-1])
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
        if hasattr(self, "cls"):
            return f"class: {self.cls}; data: {str(self.data)}"
        return f"data: {str(self.data)}"
