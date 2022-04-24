from eddm.eddm import EDDM
from window_method.Window import Window
from common.Vector import Vector
from config import SKIP_FIRST_LINE
from window_method.WindowManager import WindowManager

#window_manager = WindowManager(windows_number=2, window_size=1000, drift_threshold=0.5, step=10)
#window_manager.analyze(filename="data/dataverse/mixed_0101_gradual.csv")

eddm = EDDM()
eddm.analyze(number_to_train=100, filename="data/dataverse/mixed_0101_gradual.csv")