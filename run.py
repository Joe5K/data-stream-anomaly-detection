# -*- coding: utf-8 -*-
from eddm.eddm import EDDM
from pht_method.pht import PageHinkley
from window_method.window_manager import WindowManager

print("Page-Hinkley Test")
pht = PageHinkley(train_instances=100, threshold=35)
pht.analyze(filename="data/dataverse/sine_3210_gradual.csv")
print("_________________________________")

print("Early Drift Detection Method")
eddm = EDDM(train_instances=100, error_threshold=0.7)
eddm.analyze(filename="data/dataverse/sine_3210_gradual.csv")
print("_________________________________")

print("My own window method :)")
window_manager = WindowManager(windows_number=2, window_size=500, drift_threshold=0.2, step=10)
window_manager.analyze(filename="data/dataverse/sine_3210_gradual.csv")
print("_________________________________")
