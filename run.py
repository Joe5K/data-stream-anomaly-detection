# -*- coding: utf-8 -*-
from collections import OrderedDict
from datetime import datetime

from common.stream import DriftStream
from eddm.eddm import EDDM
from pht_method.pht import PageHinkley
from window_method.window_manager import WindowManager
from random import randint

parameters = []

while len(parameters) < 15:
    position = randint(10000, 1000000)
    width = randint(200, 200000)
    if position - width - 10000 < 0:
        continue
    parameters.append((position, width))

out = ""
eddm_time = 0
pht_time = 0
win_time = 0
tests_time = []

for i, (position, width) in enumerate(parameters):
    print(f"Test {i+1}")
    test_start = datetime.now()
    drift_stream = DriftStream(position, width)
    data = drift_stream.data()
    out += f"{i+1} & {position} & {width}"

    start = datetime.now()
    eddm = EDDM(train_instances=2000, error_threshold=0.7)
    drift = eddm.analyze(data=data)
    elapsed = (datetime.now() - start).total_seconds()
    eddm_time += elapsed
    out += f" & {drift} & {round(elapsed, 2)}"

    start = datetime.now()
    pht = PageHinkley(train_instances=2000, threshold=4500, alpha=0.999)
    drift = pht.analyze(data=data)
    elapsed = (datetime.now() - start).total_seconds()
    pht_time += elapsed
    out += f" & {drift} & {round(elapsed, 2)}"

    start = datetime.now()
    window_manager = WindowManager(windows_number=2, window_size=5000, drift_threshold=0.4, step=10)
    drift = window_manager.analyze(data=data)
    elapsed = (datetime.now() - start).total_seconds()
    win_time += elapsed
    out += f" & {drift} & {round(elapsed, 2)}"

    elapsed = (datetime.now() - test_start).total_seconds()
    out += f" & {elapsed}\\\\\n"
print(f"& & & & {round(eddm_time, 2)} & & {round(pht_time, 2)} & & {round(win_time, 2)} & {round(sum([eddm_time, pht_time, win_time]), 2)}")
