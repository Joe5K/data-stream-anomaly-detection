from typing import Dict

from common.Vector import Vector
from config import SKIP_FIRST_LINE
from numpy import mean

class EDDM:
    def __init__(self, waning_threshold=0.95, error_threshold=0.9):
        self.trained = {}
        self.means: Dict[str, Vector] = {}
        self.error_distances = []
        self.waning_threshold = waning_threshold
        self.error_threshold = error_threshold
        self.simax = 0

    def analyze(self, number_to_train: int, filename: str):
        with open(filename, "r") as reader:
            if SKIP_FIRST_LINE:
                reader.readline()
            last_error = number_to_train
            for counter, line in enumerate(reader.readlines()):
                new_vector = Vector.generate_vector(line)
                if sum(self.trained.values()) < number_to_train:
                    self.train(new_vector)
                    continue

                predicted_class = self.predict_class(new_vector)
                if predicted_class != new_vector.cls:
                    self.error_distances.append(counter - last_error)
                    last_error = counter
                self.train(new_vector)

    @property
    def error_variance(self):
        error_mean = mean(self.error_distances)

        maximum = 0
        for error in self.error_distances:
            if abs(error - mean) > maximum:
                maximum = abs(error - mean)
        return maximum

    @property
    def pimax(self):
        return max(self.error_distances)

    def train(self, new_vector: Vector):
        if not self.means.get(new_vector.cls):
            self.trained[new_vector.cls] = 0
            self.means[new_vector.cls] = Vector(["0"] * len(new_vector.data) + [new_vector.cls])

        for i in range(len(new_vector.data)):
            self.means[new_vector.cls][i] = (self.means[new_vector.cls][i]*self.trained[new_vector.cls] + new_vector[i])/(self.trained[new_vector.cls] + 1)
        self.trained[new_vector.cls] += 1

    def predict_class(self, new_vector):
        found_class = None
        shortest_distance = float("inf")

        for cls, mean in self.means.items():
            distance = mean.distance(new_vector)
            if distance < shortest_distance:
                shortest_distance = distance
                found_class = cls

        return found_class






'''train_window = Window(window_size=1000)
filename = "data/dataverse/mixed_0101_gradual.csv"


def predict_class(train: Window, data: Vector):
    found_class = None
    shortest_distance = float("inf")

    for i in train.classes:
        distance = train.means[i].distance(data)
        if distance < shortest_distance:
            shortest_distance = distance
            found_class = i
    return found_class


with open(filename, "r") as reader:
    counter = 0
    last_error_index = 0
    if SKIP_FIRST_LINE:
        reader.readline()
    while not train_window.is_loaded:
        counter += 1
        vector = Vector.generate_vector(reader.readline())
        train_window.load_vector(vector)

    for i in reader.readlines():
        counter += 1
        new_vector = Vector.generate_vector(i)
        predicted_class = predict_class(train_window, new_vector)
        if predicted_class != new_vector.cls:
            print(f"{counter}: {counter - last_error_index}")
            last_error_index = counter'''
