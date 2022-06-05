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

        stats = RunningVectorStatistics()
        stats2 = RunningVectorStatistics()
        data = []
        for index, (vector_data, cls) in enumerate(zip(*sample)):

            vector = Vector(data=vector_data.tolist(), cls=str(cls.tolist()))
            data.append(vector)

            '''if index == self.drift_position - self.drift_width:
                print("Before drift")
                print(f"Stats 1 mean: {str(stats.mean)}")
                print(f"Stats 1 var: {str(stats.variance)}")
                print(f"Stats 2 mean: {str(stats2.mean)}")
                print(f"Stats 2 var: {str(stats2.variance)}")
                stats2.reset()
            
            if index == self.drift_position + self.drift_width:
                print("After drift")
                print(f"Stats 1 mean: {str(stats.mean)}")
                print(f"Stats 1 var: {str(stats.variance)}")
                print(f"Stats 2 mean: {str(stats2.mean)}")
                print(f"Stats 2 var: {str(stats2.variance)}")
                stats2.reset()
            
            if index == self.drift_position*2-1:
                print("End drift")
                print(f"Stats 1 mean: {str(stats.mean)}")
                print(f"Stats 1 var: {str(stats.variance)}")
                print(f"Stats 2 mean: {str(stats2.mean)}")
                print(f"Stats 2 var: {str(stats2.variance)}")
                stats2.reset()

            stats.push(vector)
            stats2.push(vector)'''

        return data


