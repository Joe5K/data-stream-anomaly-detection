# -*- coding: utf-8 -*-
from common.stream import DriftStream
from eddm.eddm import EDDM
from pht_method.pht import PageHinkley
from window_method.window_manager import WindowManager

drift_position = 50000
drift_width = 5000
drift_stream = DriftStream(drift_position, drift_width)
data = drift_stream.data()


print("Page-Hinkley Test")
pht = PageHinkley(train_instances=4000, threshold=5000, alpha=0.999)
pht.analyze(data=data)
print("_________________________________")

print("Early Drift Detection Method")
eddm = EDDM(train_instances=2000, error_threshold=0.7)
eddm.analyze(data=data)
print("_________________________________")

print("My own window method :)")
window_manager = WindowManager(windows_number=2, window_size=3000, drift_threshold=0.6, step=10)
window_manager.analyze(data=data)
print("_________________________________")


