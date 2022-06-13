from skmultiflow.data import ConceptDriftStream, SEAGenerator

from common.running_stats import RunningVectorStatistics
from common.vector import Vector


class DriftStream:
    # Help class to save generated stream to a list, used for testing more methods on same data.
    def __init__(self, drift_position: int = 50000, drift_width: int = 5000):
        # The constructor.
        self.drift_position = drift_position
        self.drift_width = drift_width

    def data(self):
        # Method generating stream and returning first drift_position*2 values as list of vectors
        sample = ConceptDriftStream(
            stream=SEAGenerator(classification_function=3),
            drift_stream=SEAGenerator(classification_function=2),
            position=self.drift_position,
            width=self.drift_width
        ).next_sample(batch_size=self.drift_position*2)

        data = []
        for index, (vector_data, cls) in enumerate(zip(*sample)):
            vector = Vector(data=vector_data.tolist(), cls=str(cls.tolist()))
            data.append(vector)

        return data


