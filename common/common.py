from datetime import datetime


def get_cur_time_str():
    return datetime.now().strftime('%H:%M:%S.%f')