# -*- coding: utf-8 -*-
from typing import List, Tuple

WINDOW_SIZE = 50
WINDOWS_NUMBER = 2
SEPARATOR = ","
SKIP_FIRST_LINE = True
LAST_COL_IS_CLASS = True


class Vector:
    def __init__(self, data: List[str]):
        if LAST_COL_IS_CLASS:
            self.data = tuple([float(i) for i in data[:-1]])
            self.cls = data[-1]

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index) -> float:
        if index < len(self):
            return self.data[index]

    def __iter__(self) -> iter:
        return iter(self.data)

    def __repr__(self) -> str:
        return f"class: {self.cls}; data: {str(self.data)}"


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
    def mean(self) -> Tuple[float]:
        sum_vector = [0] * len(self.data[0])
        for vector in self.data:
            for index, data in enumerate(vector):
                sum_vector[index] += data

        return tuple([i / len(self.data) for i in sum_vector])

    @property
    def variance(self) -> Tuple[float]:
        variance_vector = [0] * len(self.data[0])
        for vector in self.data:
            for index, data in enumerate(vector):
                variance_vector[index] += (data - self.mean[index]) ** 2

        return tuple([i / len(self.data) for i in variance_vector])

    def __repr__(self) -> str:
        return str(self.mean)


class WindowManager:
    def __init__(self):
        self.windows: List[Window] = []

    def analyze(self, filename: str):
        with open(filename, "r") as input_stream:
            if SKIP_FIRST_LINE:
                input_stream.readline()

            for i in range(WINDOWS_NUMBER):
                window = Window()
                while not window.is_loaded:
                    window.load_line(input_stream.readline())
                self.windows.append(window)


# TDO rozlisovanie mean a variance a dalsich podla classy
WindowManager().analyze("data/dataverse/mixed_0101_gradual.csv")
