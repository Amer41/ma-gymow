import math

def extract_feature_vector(Cs_fourier_coefficients: list[complex]) -> list[float]:
    feature_vector: list[float] = []
    for c in Cs_fourier_coefficients:
        length = math.sqrt(c.real**2 + c.imag**2)
        feature_vector.append(length)
    return feature_vector

def compute_distance(feature_vector_1: list[float], feature_vector_2: list[float]):
    N = len(feature_vector_1)
    d2 = 0
    for i in range(N):
        d2 += (feature_vector_1[i] - feature_vector_2[i])**2
    d2 = math.sqrt(d2)
    return d2
