from skmultiflow.data import ConceptDriftStream, SEAGenerator

from common.running_stats import RunningVectorStatistics
from common.vector import Vector


class DriftStream:
    def __init__(self, drift_position: int = 50000, drift_width: int = 5000):
        self.drift_position = drift_position
        self.drift_width = drift_width

    def data(self):
        sample = ConceptDriftStream(
            stream=SEAGenerator(classification_function=3),
            drift_stream=SEAGenerator(classification_function=2),
            position=self.drift_position,
            width=self.drift_width
        ).next_sample(batch_size=self.drift_position*2)

        data = []
        for index, (vector_data, cls) in enumerate(zip(*sample)):
            data.append(Vector(data=vector_data.tolist(), cls=cls.tolist()))

        return data


