# -*- coding: utf-8 -*-
from collections import OrderedDict

from common.stream import DriftStream
from eddm.eddm import EDDM
from pht_method.pht import PageHinkley
from window_method.window_manager import WindowManager

'''for drift_width in [2000, 5000, 8000, 13000]:
    drift_position = 50000
    drift_start = drift_position - drift_width/2
    drift_end = drift_start + drift_width
    drift_stream = DriftStream(drift_position, drift_width)

    for x in range(4):
        data = drift_stream.data()
        best_threshold = None
        best_distance = drift_position
        for i in range(50, 80, 1):
            threshold = i / 100
            eddm = EDDM(train_instances=2000, error_threshold=threshold)
            drift_index = eddm.analyze(data=data) or 0
            if abs(drift_index - drift_end) < best_distance:
                best_threshold = threshold
                best_distance = abs(drift_index - drift_end)
        print(f"EDDM Width {drift_width}: Best threshold:{best_threshold}; distance from drift_end: {best_distance}")'''


'''for drift_width in [2000, 5000, 8000, 13000]:
    drift_position = 50000
    drift_start = drift_position - drift_width/2
    drift_end = drift_start + drift_width
    drift_stream = DriftStream(drift_position, drift_width)

    for x in range(4):
        data = drift_stream.data()
        best_threshold = None
        best_distance = drift_position
        for i in range(4000, 5000, 50):
            threshold = i / 1
            pht = PageHinkley(train_instances=2000, threshold=threshold, alpha=0.999)
            drift_index = pht.analyze(data=data) or 0
            if abs(drift_index - drift_position) < best_distance:
                best_threshold = threshold
                best_distance = abs(drift_index - drift_position)
        print(f"PHT Width {drift_width}: Best threshold:{best_threshold}; distance from drift_end: {best_distance}")
'''

sums = OrderedDict()
count = 0
str1 = ""
str2 = ""
for x in range(4):
    count += 1
    str1 += str(count)
    str2 += str(count)
    for drift_width in [2000, 5000, 8000, 13000, 25000]:
        drift_position = 50000
        drift_start = drift_position - drift_width / 2
        drift_end = drift_start + drift_width
        drift_stream = DriftStream(drift_position, drift_width)
        data = drift_stream.data()

        window_manager = WindowManager(windows_number=2, window_size=5000, drift_threshold=0.4, step=10)
        drift_index = window_manager.analyze(data=data) or 0

        val1 = str(round((drift_index-drift_position)/drift_width, 2)).replace('.', ',')
        while len(val1) < 4:
            val1 += "0"
        str1 += f" & {val1}"
        str2 += f" & {str(int(drift_index-drift_start)).replace('.',',')}"

        #print(f"{drift_width} - detected after {drift_index-drift_start}, relatively {(drift_index-drift_start)/drift_width}. ({drift_index})")

    str1 += "\\\\\n"
    str2 += "\\\\\n"

print(str1)
print(str2)
'''

drift_stream = DriftStream(50000, 2000)
data = drift_stream.data()

print("Page-Hinkley Test")
pht = PageHinkley(train_instances=2000, threshold=5000, alpha=0.999)
pht.analyze(data=data)
print("_________________________________")

print("Early Drift Detection Method")
eddm = EDDM(train_instances=2000, error_threshold=0.7)
eddm.analyze(data=data)
print("_________________________________")

print("My own window method :)")
window_manager = WindowManager(windows_number=2, window_size=5000, drift_threshold=0.35, step=10)
window_manager.analyze(data=data)
print("_________________________________")

'''