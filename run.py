# -*- coding: utf-8 -*-
from eddm.eddm import EDDM
from window_method.window_manager import WindowManager

#window_manager = WindowManager(windows_number=2, window_size=1000, drift_threshold=0.5, step=10)
#window_manager.analyze(filename="data/dataverse/mixed_0101_gradual.csv")

eddm = EDDM()
eddm.analyze(number_to_train=100, filename="data/dataverse/mixed_1010_gradual.csv")
