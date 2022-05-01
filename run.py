# -*- coding: utf-8 -*-
from eddm.eddm import EDDM
from pht_method.pht import PageHinkley
from window_method.window_manager import WindowManager

print("Page-Hinkley Test")
pht = PageHinkley(window_size=100)
pht.analyze(filename="data/dataverse/mixed_1010_gradual.csv")
print("_________________________________")

print("Early Drift Detection Method")
eddm = EDDM()
eddm.analyze(number_to_train=100, filename="data/dataverse/mixed_1010_gradual.csv")
print("_________________________________")

print("My own window method :)")
window_manager = WindowManager(windows_number=2, window_size=500, drift_threshold=0.3, step=10)
window_manager.analyze(filename="data/dataverse/mixed_1010_gradual.csv")
print("_________________________________")
