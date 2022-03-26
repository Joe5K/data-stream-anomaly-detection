# -*- coding: utf-8 -*-
from io import TextIOWrapper
from typing import List, TextIO, Optional

from config import SKIP_FIRST_LINE, WINDOWS_NUMBER
from app.Window import Window


class WindowManager:
    def __init__(self):
        self.windows: List[Window] = []
        self.input_stream: Optional[TextIO] = None

    def initialize(self):
        if SKIP_FIRST_LINE:
            self.input_stream.readline()

        for i in range(WINDOWS_NUMBER):
            window = Window()
            while not window.is_loaded:
                window.load_line(self.input_stream.readline())
            self.windows.append(window)

    def analyze(self, filename: str):
        with open(filename, "r") as input_stream:
            self.input_stream = input_stream
            self.initialize()
            #TODO nacitavanie dalsich dat, porovnavanie s windows, posuvanie windows

WindowManager().analyze("data/dataverse/mixed_0101_gradual.csv")
