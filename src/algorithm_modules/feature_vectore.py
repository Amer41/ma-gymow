import math
import numpy as np

from typing import Any

def compute_FSC_v3(coefficients_number: int, f: list[float]) -> tuple[tuple[list[float], list[float]], list[complex]]: # berechnet Fourier-Koeffizienten (a, b und c)
    N = len(f)
    T = math.pi
    w = 2 #* math.pi / T
    dt = T / (N)
    t = [i*dt for i in range(N)]
    coeff_number = coefficients_number + 1
    As: list[float] = []
    Bs: list[float] = []
    Cs: list[complex] = []
    for n in range(coeff_number):
        a_n: float = 0
        b_n: float = 0
        for i in range(N):
            phi = n*w*t[i]
            a_n += f[i] * math.cos(phi) * dt
            b_n += f[i] * math.sin(phi) * dt
        a_n *= (2 / T)
        b_n *= (2 / T)
        As.append(a_n)
        Bs.append(b_n)
        Cs.append((1/2) * (a_n - 1j*b_n))
        Cs.append((1/2) * (a_n + 1j*b_n))
    del Cs[0]
    As[0] /= 2
    return (As, Bs), Cs
# def compute_FSC_v3(coefficients_number, f): # wie oben aber ohne duplikate
#     N = len(f)
#     T = math.pi
#     w = 2 #* math.pi / T
#     dt = T / (N)
#     t = [i*dt for i in range(N)]


#     coeff_number = coefficients_number


#     As = []
#     Bs = []
#     Cs = []
#     for n in range(coeff_number):
#         a_n = 0
#         b_n = 0
#         for i in range(N):
#             phi = n*w*t[i]
#             a_n += f[i] * math.cos(phi) * dt
#             b_n += f[i] * math.sin(phi) * dt
#         a_n *= (2 / T)
#         b_n *= (2 / T)
#         As.append(a_n)
#         Bs.append(b_n)
#         Cs.append((1/2) * (a_n - 1j*b_n))


#     #     Cs.append((1/2) * (a_n + 1j*b_n))
#     # del Cs[0]


#     As[0] /= 2
#     return (As, Bs), Cs
        
def invert_FSC_v3(number_of_points: int, C: tuple[list[float], list[float]]) -> list[float]: # rekonstruiert R aus Fourier-Koeffizienten
    As = C[0]
    Bs = C[1]
    N = number_of_points
    T = math.pi
    w = 2
    dt = T / (N)
    t = [i*dt for i in range(N)]
    coeff_number = len(As)
    F: list[float] = []
    for i in range(N):
        f_t = 0
        for n in range(coeff_number):
            phi = n * w * t[i]
            f_t += (As[n] * math.cos(phi)) + (Bs[n] * math.sin(phi))
        F.append(f_t)
    return F

def extract_feasure_vector_v3(Cs: list[complex]) -> list[float]: # Merkmalsvektor wird erstellt, fv = merkmalsvektor
    fv: list[float] = []
    for c in Cs:
        length = math.sqrt(c.real**2 + c.imag**2)
        fv.append(length)
    return fv

def compute_distance_2_v3(fv1: list[float], fv2: list[float]):
    N = len(fv1)
    d2 = 0
    for i in range(N):
        d2 += (fv1[i] - fv2[i])**2
    d2 = math.sqrt(d2)
    return d2
