# -*- coding: utf-8 -*-
from math import sqrt
from typing import List

from window_method.Vector import Vector
from config import SKIP_FIRST_LINE
from window_method.Window import Window


class WindowManager:
    def __init__(self, windows_number: int, window_size: int, drift_threshold: float):
        self.windows: List[Window] = []
        self.windows_number = windows_number
        self.window_size = window_size
        self.drift_threshold = drift_threshold

    def initialize(self, input_stream):
        if SKIP_FIRST_LINE:
            input_stream.readline()

        for i in range(self.windows_number):
            window = Window(self.window_size)
            while not window.is_loaded:
                new_vector = Vector.generate_vector(input_stream.readline())
                window.load_vector(new_vector)
            self.windows.append(window)

    def compare_windows_means(self, first: int, second: int):
        first_window = self.windows[first]
        second_window = self.windows[second]

        sum = 0
        for cls in {*first_window.classes, *second_window.classes}:
            for i, j in zip(first_window.mean[cls], second_window.mean[cls]):
                sum += (i - j) ** 2
        return sqrt(sum)

    def move(self, input_data: str):
        new_vector = Vector.generate_vector(input_data)
        drift_found = False
        for count, window in enumerate(self.windows[::-1]):
            index = len(self.windows) - 1 - count
            if index > 0:
                before = self.compare_windows_means(index, index-1)
            new_vector = window.load_vector(new_vector)
            if index > 0:
                after = self.compare_windows_means(index, index-1)
                if after > self.drift_threshold:
                    print("CHANGE") # TODO premazat windows a reinicializovat
            pass
           # print(variation)  # TODO hladanie posunov, skor porovnavanie jednotlivych windows nez len aktualnych dat

        #print(f"Popping old vector: {new_vector}")

    def analyze(self, filename: str):
        with open(filename, "r") as input_stream:
            for line in input_stream.readlines():
                pass  # TODO zobecnit, pre buduce premazavanie windows a novu inicializaciu
            self.initialize(input_stream)

            while input_data := input_stream.readline():
                self.move(input_data)

    @property
    def is_initialized(self):
        for window in self.windows:
            if not window.is_loaded:
                return False
        return True