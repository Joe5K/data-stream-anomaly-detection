# -*- coding: utf-8 -*-
from collections import OrderedDict
from datetime import datetime

from common.stream import DriftStream
from eddm.eddm import EDDM
from pht_method.pht import PageHinkley
from window_method.window_manager import WindowManager
from random import randint

parameters = []

#parameters.append((10000, 2000))
while len(parameters) < 15:# and False:
    position = randint(10000, 1000000)
    width = randint(200, 200000)
    if position - width - 10000 < 0:
        continue
    position_sub = max(len(str(position)) - 3, 0)
    position = round(position / 10**position_sub)*10**position_sub

    width_sub = max(len(str(width)) - 3, 0)
    width = round(width / 10 ** width_sub) * 10 ** width_sub

    parameters.append((position, width))


def process(number, left=None, right=None):
    ret = None

    if isinstance(number, int):
        krista = str(number)
        ret = ""
        for index, letter in enumerate(krista[::-1]):
            ret = letter + ret
            if index % 3 == 2 and index + 1 != len(krista):
                ret = "{ }" + ret
    if isinstance(number, float):
        ret = str(round(number, 2))
        while len(ret) - ret.find(".") < 3:
            ret += "0"

    if isinstance(left, bool) and isinstance(right, bool):
        if left:
            ret = "\\textcolor{red}{" + ret + "}"
        elif right:
            ret = "\\textcolor{myorange}{" + ret + "}"
        else:
            ret = "\\textcolor{mygreen}{" + ret + "}"


    return ret


out = ""
out2 = ""
eddm_time = 0
pht_time = 0
win_time = 0
eddm_mimo = pht_mimo = win_mimo = 0


for i, (position, width) in enumerate(parameters):
    print(f"Test {i+1} with position {position} and width {width}, so drift at <{int(position-width/2)}; {int(position+width/2)}>")
    test_start = datetime.now()
    drift_stream = DriftStream(position, width)
    drift_start = int(position-width/2)
    drift_end = int(position+width/2)
    data = drift_stream.data()
    out += f"{i+1} & {process(position)} & {process(width)}"
    out2 += f"{i+1} & {process(drift_start)} & {process(drift_end)}"

    start = datetime.now()
    eddm = EDDM(train_instances=2000, error_threshold=0.7)
    drift = eddm.analyze(data=data)
    elapsed = (datetime.now() - start).total_seconds()
    eddm_time += elapsed
    eddm_mimo += abs(drift - position)
    out += f" & {process(drift)} & {process(elapsed, 2)}"
    out2 += f" & {process(drift, left=drift_start>drift, right=drift>drift_end)}"
    print(f"Got EDDM with drift at {drift} in {round(elapsed, 2)}")

    start = datetime.now()
    pht = PageHinkley(train_instances=2000, threshold=4500, alpha=0.999)
    drift = pht.analyze(data=data)
    elapsed = (datetime.now() - start).total_seconds()
    pht_time += elapsed
    pht_mimo += abs(drift - position)
    out += f" & {process(drift)} & {process(elapsed, 2)}"
    out2 += f" & {process(drift, left=drift_start > drift, right=drift > drift_end)}"
    print(f"Got PHT with drift at {drift} in {round(elapsed, 2)}")

    start = datetime.now()
    window_manager = WindowManager(windows_number=2, window_size=5000, drift_threshold=0.4, step=10)
    drift = window_manager.analyze(data=data)
    elapsed = (datetime.now() - start).total_seconds()
    win_time += elapsed
    win_mimo += abs(drift - position)
    out += f" & {process(drift)} & {process(elapsed, 2)}"
    out2 += f" & {process(drift, left=drift_start > drift, right=drift > drift_end)}"
    print(f"Got Window with drift at {drift} in {round(elapsed, 2)}")

    elapsed = (datetime.now() - test_start).total_seconds()
    out2 += f"\\\\\n"
    out += f" & {process(elapsed, 2)}\\\\\n"
print(f"{out}\\hline\n\\(\\sum\\) Čas & & & & {process(eddm_time, 2)} & & {process(pht_time, 2)} & & {process(win_time, 2)} & {process(sum([eddm_time, pht_time, win_time]), 2)}\\\\".replace('.', ','))
print(out2)
print(f"Average distance from positions: eddm {eddm_mimo/15}, pht {pht_mimo/15}, win {win_mimo/15}")
