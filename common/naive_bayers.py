import math

from common.vector import Vector


def naive_bayers_distance(vector: Vector, mean: Vector, variance: Vector, initial_probability: int = 1):
    # Count distance for naive bayers classifier between a vector and concrete classification mean and variance.
    probability = initial_probability
    for x, u, o2 in zip(vector, mean, variance):
        probability *= (1 / (math.sqrt(2 * math.pi) * math.sqrt(o2))) * math.exp(-((x - u) ** 2) / (2 * o2))

    return probability
