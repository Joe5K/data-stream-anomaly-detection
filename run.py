import csv
import math
from math import sqrt, pi, exp
from decimal import Decimal


def matrix_to_float(matrix: list) -> list:
    matrix_out = []
    for i in matrix:
        matrix_out.append([float(j) for j in i])
    return matrix_out


def transpose_matrix(matrix: list) -> list:
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


def count_mean(data: list) -> float:
    mean = 0
    for i in data:
        mean += i
    return mean/len(data)


def count_variance(data: list, mean: float) -> float:
    variance = 0
    for i in data:
        variance += (i - mean)**2
    return variance/len(data)


def count_mean_and_variance_of_matrix(data):
    transposed_data = transpose_matrix([i for i in data if i[-1] != 1])
    means = []
    variances = []
    for i in transposed_data[:-1]:
        if transposed_data[-1] == 1:
            continue
        mean = count_mean(i)
        means.append(mean)
        variance = count_variance(i, mean)
        variances.append(variance)

    return means, variances


def get_anomalies(data: list, mean: list, variance: list):
    epsylon = 0
    for row in data:
        row_anomaly = Decimal(1)
        for i, (x, u, o) in enumerate(zip(row, mean, variance)):
            if o == 0 or u == x:
                continue
            row_anomaly *= Decimal((1/(sqrt(2*pi)*o)) * exp(-((x-u)**2)/(2*(o**2))))  # tu je cosi dojebane
        print(row_anomaly)


with open('data/Participants_Data_WH18/Train.csv', newline='') as csvfile:
    train = list(csv.reader(csvfile))
    means, variances = count_mean_and_variance_of_matrix(matrix_to_float(train[1:]))

with open('data/Participants_Data_WH18/Test.csv', newline='') as csvfile:
    test = list(csv.reader(csvfile))
    get_anomalies(matrix_to_float(test[1:]), means, variances)

