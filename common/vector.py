# -*- coding: utf-8 -*-
import math
from typing import Union, Optional, Iterable

from config import SEPARATOR


class Vector:
    # Vector class used by all methods, contains data and optionally their classification.

    def __init__(self, data: Iterable[Union[str, float]], cls: Optional[str] = None):
        # The constructor.
        self.data = list(float(i) for i in data)
        self.cls = cls

    def distance(self, other_vector):
        # Counts distance between self and other vector.
        sum = 0
        for i, j in zip(self, other_vector):
            sum += (i - j)**2
        return math.sqrt(sum)

    def __len__(self) -> int:
        # len(vector) returns size of a vector.
        return len(self.data)

    def __getitem__(self, key) -> float:
        # Get vector value at index key.
        if key < len(self):
            return self.data[key]

    def __setitem__(self, key, value):
        # Set vector value at index key.
        if key < len(self):
            self.data[key] = value

    def __iter__(self) -> iter:
        # Help method to iterate through vector data.
        return iter(self.data)

    def __repr__(self) -> str:
        # Help method to write vector as string.
        if self.cls:
            return f"class: {self.cls}; data: {str(self.data)}"
        return f"data: {str(self.data)}"
