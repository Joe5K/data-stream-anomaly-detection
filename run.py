# -*- coding: utf-8 -*-
from common.stream import DriftStream
from eddm.eddm import EDDM
from pht_method.pht import PageHinkley
from window_method.window_manager import WindowManager

drift_stream = DriftStream(drift_position=40000, drift_width=2000)
data = drift_stream.data()

print("Page-Hinkley Test")
pht = PageHinkley(train_instances=2000, threshold=600, alpha=0.99, delta=0.45)
pht.analyze(data=data)
print("_________________________________")

print("Early Drift Detection Method")
eddm = EDDM(train_instances=2000, error_threshold=0.65)
eddm.analyze(data=data)
print("_________________________________")

print("My own window method :)")
window_manager = WindowManager(windows_number=2, window_size=2000, drift_threshold=0.6, step=10)
window_manager.analyze(data=data)
print("_________________________________")


