from src.algorithm_modules.vector3 import vec3
from src.algorithm_modules.matrix3 import Matrix3
import numpy.linalg as npl
import numpy as np
import math
# Die Funktionen enthalten v3 im Namen als Indikator dafür, dass sie mit
# dem Datenformat vec3 (die oben erstellte klasse) arbeiten

# Die Beschriftung der Mengen ist konsequent gehalten im ganzen Dokument
# hier wird erklärt, welche beschriftung was heisst.

def compute_T_v3(V: list[vec3], F: list[tuple[int, int, int]]) -> list[vec3]: # combiniert V und F und erstellt die Menge aller Facetten (Dreiecke T)
    T: list[vec3] = []
    for f in F:
        f1, f2, f3 = f
        T.append(V[f1])
        T.append(V[f2])
        T.append(V[f3])
    return T

def compute_S_v3(T: list[vec3]) -> tuple[list[float], float]: # berechnet die Oberflächen aller Dreiecke S und die gesamtoberfläche des Modells S_total
    S_total = 0
    S: list[float] = []
    n = int(len(T) /3)
    for i in range(n):
        ii = 3 * i
        v_0 = T[ii + 0]
        v_1 = T[ii + 1]
        v_2 = T[ii + 2]
        normal = v_2.sub(v_0).cross(v_1.sub(v_0))
        s = normal.length() * 0.5
        S_total += s
        S.append(s)
    return S, S_total

def compute_G_v3(T: list[vec3]) -> list[vec3]: # bestimmt die Schwerpunkte aller Dreiecke G
    G: list[vec3] = []
    n = int(len(T) /3)
    
    for i in range(n):
        ii = 3 * i
        v_0 = T[ii + 0]
        v_1 = T[ii + 1]
        v_2 = T[ii + 2]
        c_x = (v_0.x + v_1.x + v_2.x) / 3
        c_y = (v_0.y + v_1.y + v_2.y) / 3
        c_z = (v_0.z + v_1.z + v_2.z) / 3
        G.append(vec3(c_x, c_y, c_z))
    return G

def compute_m_I_v3(S: list[float], S_total: float, G: list[vec3]) -> vec3: # bestimmt der SChwerpunkt des gesamten 3D-Modells m_I
    M = vec3(0, 0, 0)
    for i in range(len(S)):
        M.sumup(G[i].multiply_scalar(S[i]))
    m_I = M.multiply_scalar(1/S_total)
    return m_I


def compute_T_S_G_m_I_v3(V: list[vec3], F: list[tuple[int, int, int]]) -> tuple[list[vec3], list[float], float, list[vec3], vec3, list[vec3]]: # die oberen 4 Funktionen werden kombiniert, um Anzahl Iterationen zu verringern
    T: list[vec3] = []
    S_total = 0
    S: list[float] = []
    G: list[vec3] = []
    M = vec3(0, 0, 0)
    normals: list[vec3] = []
    for i in range(len(F)):
        f1, f2, f3 = F[i]
        v_0, v_1, v_2 = V[f1], V[f2], V[f3]
        T.append(v_0)
        T.append(v_1)
        T.append(v_2)

        normal = v_2.sub(v_0).cross(v_1.sub(v_0))
        normals.append(normal)
        s = normal.length() * 0.5
        S_total += s
        S.append(s)

        c_x = (v_0.x + v_1.x + v_2.x) / 3
        c_y = (v_0.y + v_1.y + v_2.y) / 3
        c_z = (v_0.z + v_1.z + v_2.z) / 3
        g = vec3(c_x, c_y, c_z)
        G.append(g)

        M.sumup(G[i].multiply_scalar(s))
    m_I = M.multiply_scalar(1/S_total)
    return T, S, S_total, G, m_I, normals
    
def shift_V_v3(V: list[vec3], m_I: vec3) -> list[vec3]: # Zentriert das 3d-Modell, V1 = Menge der zentrierten Eckpunkte
    V1: list[vec3] = []
    for v in V:
        V1.append(v.sub(m_I))
    return V1

def compute_C_I_v3(S: list[float], S_total: float, G1: list[vec3], T1:list[vec3]) -> Matrix3: # berechnet die Kovarianzmatrix des Modells C_I
    n = int(len(T1) /3)
    c_I = Matrix3(
        0,0,0,
        0,0,0,
        0,0,0
    )
    for i in range(n):
        ii = 3 * i
        v_0 = T1[ii + 0]
        v_1 = T1[ii + 1]
        v_2 = T1[ii + 2]
        g = G1[i]
        c = g.covariance_matrix(g).multiply_with_scalar(9)
        c.sumup(v_0.covariance_matrix(v_0))
        c.sumup(v_1.covariance_matrix(v_1))
        c.sumup(v_2.covariance_matrix(v_2))
        c_I.sumup(c.multiply_with_scalar(S[i]))
    c_I = c_I.multiply_with_scalar(1/(12 * S_total))
    return c_I

def compute_eigs_v3(c_I_1: Matrix3) -> tuple[vec3, Matrix3]: # bestimmt eigenvekoren und eigenwerte von C_I (über numpy)
    c_I = c_I_1.to_array()
    eig_values, eig_vectors = npl.eig(c_I) # type: ignore
    
    sorted_indices = np.argsort(eig_values) # type: ignore
    eig_vec_T = eig_vectors.T # type: ignore
    A = np.zeros((3,3))  # type: ignore
    sorted_eig_values = np.zeros((1,3))[0] # type: ignore
    for i in range(len(A)): # type: ignore
        ii = sorted_indices[2-i]
        A[i] = eig_vec_T[ii] # type: ignore
        sorted_eig_values[i] = eig_values[ii]
    eigs = vec3.from_array(sorted_eig_values), Matrix3.from_array(A) # type: ignore
    return eigs

def rotate_V1_v3(V1: list[vec3], A: Matrix3) -> list[vec3]: # rotiert V1, V2 = die verschobenen und dann rotierten Eckpunkte
    V2: list[vec3] = []
    for v in V1:
        # v = V1[i]
        v2 = v.multiply_matrix3(A)
        # v2 = A.multiply_vec3(v)
        V2.append(v2)
    return V2

    
def compute_flipping_v3(T2: list[vec3], S: list[float], S_total: float) -> vec3: # Reflektionsmatrix Fl wird erstellt
    n = int(len(T2) / 3)
    fx = 0
    fy = 0
    fz = 0
    Fxyz: list[float] = [0, 0, 0]
    for i in range(n):
        s = S[i]
        ii = i * 3
        v_0 = T2[ii + 0]
        v_1 = T2[ii + 1]
        v_2 = T2[ii + 2]
        x_0, y_0, z_0 = v_0.x, v_0.y, v_0.z
        x_1, y_1, z_1 = v_1.x, v_1.y, v_1.z
        x_2, y_2, z_2 = v_2.x, v_2.y, v_2.z
        x = (x_0, x_1, x_2)
        y = (y_0, y_1, y_2)
        z = (z_0, z_1, z_2)
        xyz = [sorted(x), sorted(y), sorted(z)]
        for k in range(3):
            x1, x2, x3 = xyz[k]
            J = (x1**2 + x2**2 + x3**2 + x1*x2 + x1*x3 + x2*x3)
            if x1 >= 0 and x2 >= 0 and x3 >= 0:
                Fxyz[k] = J
            elif x1 < 0 and x2 < 0 and x3 < 0:
                Fxyz[k] = -J
            elif x1  < 0 and x2 >= 0 and x3 >= 0:
                Lx = (x1**4) / ((x2-x1)*(x3-x1))
                Fxyz[k] = J - 2*Lx
            elif x3 >= 0 and x1 < 0 and x2 < 0:
                Lx = (x3**4) / ((x2-x3)*(x1-x3))
                Fxyz[k] = -J + 2*Lx
            else:
                print('error')
        fx += Fxyz[0] * s
        fy += Fxyz[1] * s
        fz += Fxyz[2] * s
    fx /= 6*S_total
    fy /= 6*S_total
    fz /= 6*S_total
    sign_x = math.copysign(1, fx)
    sign_y = math.copysign(1, fy)
    sign_z = math.copysign(1, fz)
    Fl = vec3(sign_x, sign_y, sign_z)
    return Fl

def compute_scale_v3(T2: list[vec3], S: list[float], S_total: float, p_min: int) -> float: # skalierungsfaktor d wird berechnet
    n = int(len(T2) / 3)
    d = 0
    for i in range(n):
        s = S[i]
        if s == 0:
            p_j = 1
        else:
            s = S[i]
            p_j = int(math.ceil(math.sqrt(p_min*s/S_total)))
        ii = i * 3
        a = T2[ii + 0]
        b = T2[ii + 1]
        c = T2[ii + 2]
        denom = 1/p_j
        d_ab = (b.sub(a)).multiply_scalar(denom)
        d_ac = (c.sub(a)).multiply_scalar(denom)
        d_g = (d_ab.add(d_ac)).multiply_scalar(1/3)
        gamma = s / ((p_j)**2)
        for x in range(p_j - 1):
            for y in range(x+1):
                g = a.add(d_ab.multiply_scalar((x-y)).add(d_ac.multiply_scalar(y).add(d_g)))
                d += gamma*(g.length() + (g.add(d_g)).length())
        for y in range(p_j):
            g = a.add(d_ab.multiply_scalar(p_j-1-y).add(d_ac.multiply_scalar(y).add(d_g)))
            d += gamma*g.length()
    d *= 1/S_total
    return d


def compute_V3_v3(V2: list[vec3], Fl: vec3, scale: float) -> list[vec3]: # V2 wird skaliert und eventuel reklektiert --> V3
    V3: list[vec3] = []
    s = 1 / scale
    for v in V2:
        v3 = v.multiply_vec3(Fl).multiply_scalar(s)
        V3.append(v3)
    return V3
