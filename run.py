from window_method.WindowManager import WindowManager

window_manager = WindowManager(windows_number=2, window_size=1000, drift_threshold=0.5, step=10)
window_manager.analyze("data/dataverse/mixed_0101_gradual.csv")
