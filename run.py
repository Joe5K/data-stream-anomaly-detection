# -*- coding: utf-8 -*-
from io import TextIOWrapper
from typing import List, TextIO, Optional

from app.Vector import Vector
from config import SKIP_FIRST_LINE, WINDOWS_NUMBER
from app.Window import Window


class WindowManager:
    def __init__(self):
        self.windows: List[Window] = []

    def initialize(self, input_stream):
        if SKIP_FIRST_LINE:
            input_stream.readline()

        for i in range(WINDOWS_NUMBER):
            window = Window()
            while not window.is_loaded:
                new_vector = Vector.generate_vector(input_stream.readline())
                window.load_vector(new_vector)
            self.windows.append(window)

    def compare_windows(self, first: int, second: int):
        first_window = self.windows[first]
        second_window = self.windows[second]
        return first_window.variance_distance(second_window)


    def move(self, input_data: str):
        new_vector = Vector.generate_vector(input_data)
        for count, window in enumerate(self.windows[::-1]):
            index = len(self.windows) - 1 - count
            if index > 0:
                self.compare_windows(index, index-1)
            new_vector = window.load_vector(new_vector)
            if index > 0:
                self.compare_windows(index, index-1)
           # print(variation)  # TODO hladanie posunov, skor porovnavanie jednotlivych windows nez len aktualnych dat

        print(f"Popping old vector: {new_vector}")

    def analyze(self, filename: str):
        with open(filename, "r") as input_stream:
            self.initialize(input_stream)

            while input_data := input_stream.readline():
                self.move(input_data)


window_manager = WindowManager()
window_manager.analyze("data/dataverse/mixed_0101_gradual.csv")
