import math

def compute_fourier_coefficients(coefficients_number: int, signal: list[float]) -> tuple[tuple[list[float], list[float]], list[complex]]:
    N = len(signal)
    period_length = math.pi
    w = 2 #* math.pi / T
    dt = period_length / (N)
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
            a_n += signal[i] * math.cos(phi) * dt
            b_n += signal[i] * math.sin(phi) * dt
        a_n *= (2 / period_length)
        b_n *= (2 / period_length)
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
        
def invert_FSC(number_of_points: int, As_and_Bs_fourier_coefficents: tuple[list[float], list[float]]) -> list[float]: # rekonstruiert R aus Fourier-Koeffizienten
    As = As_and_Bs_fourier_coefficents[0]
    Bs = As_and_Bs_fourier_coefficents[1]
    N = number_of_points
    T = math.pi
    w = 2
    dt = T / (N)
    t = [i*dt for i in range(N)]
    coeff_number = len(As)
    original_signal: list[float] = []
    for i in range(N):
        f_t = 0
        for n in range(coeff_number):
            phi = n * w * t[i]
            f_t += (As[n] * math.cos(phi)) + (Bs[n] * math.sin(phi))
        original_signal.append(f_t)
    return original_signal
