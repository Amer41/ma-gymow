from src.utils.curve import compute_U_v3, compute_X_and_R_from_T_devided_v3
from src.utils.cPCA import shift_V_v3, compute_T_v3, compute_C_I_v3,compute_eigs_v3, rotate_V1_v3, compute_T_S_G_m_I_v3, compute_flipping_v3, compute_scale_v3, compute_V3_v3
from src.utils.feature_vectore import compute_FSC_v3, invert_FSC_v3, extract_feasure_vector_v3
from src.utils.parsing import read_obj_v3
from src.utils.PSB import read_off
from src.modules.vector3 import vec3
import matplotlib.pyplot as plt
import numpy as np
import math
import ipyvolume as ipv
# from sre


class object2: # dtype vec3
    number_of_points = 15000 # Anzahl Punkte auf der 3D-Kurve
    winding_speed = 200 # Windungszahl
    p_min = 64000 # wird für die bestimmung des Skalierungsfaktors verwendet
    c_number = 300 # Bestimmt Anzahl Fourier-Koeffizienen im Merkmalsvektor
    plot_scale_U = 5 # skalierung für die visualisierung
    U = compute_U_v3(number_of_points, winding_speed)
    def __init__(self, V: list[vec3], F: list[tuple[int, int, int]]):
        self.V = V
        self.F = F

        # normalisierung
        self.T, self.S, self.S_total, self.G, self.m_I, self.normals1  = compute_T_S_G_m_I_v3(self.V, self.F)
        self.V1 = shift_V_v3(self.V, self.m_I)
        self.T1 = compute_T_v3(self.V1, self.F)
        self.G1 = shift_V_v3(self.G, self.m_I)
        self.C_I = compute_C_I_v3(self.S, self.S_total, self.G1, self.T1)
        self.eig_values, self.A = compute_eigs_v3(self.C_I)
        self.V2 = rotate_V1_v3(self.V1, self.A)
        self.T2 = compute_T_v3(self.V2, self.F)
        self.Fl = compute_flipping_v3(self.T2, self.S, self.S_total)
        self.scale = compute_scale_v3(self.T2, self.S, self.S_total, object2.p_min)
        self.V3 = compute_V3_v3(self.V2, self.Fl, self.scale)

        # extrahierung des Merkmalsvektors fv
        self.X, self.R = compute_X_and_R_from_T_devided_v3(object2.U, self.V3, self.F)
        (self.As, self.Bs), self.Cs = compute_FSC_v3(object2.c_number, self.R)
        self.R_real = invert_FSC_v3(object2.number_of_points, (self.As, self.Bs))
        self.fv = extract_feasure_vector_v3(self.Cs)


    # Polygonnetze können aus OBJ oder OFF gelesen werden
    @classmethod
    def from_obj(cls, obj_file: str):
        V, F = read_obj_v3(obj_file)
        return cls(V, F)
    @classmethod
    def from_off(cls, obj_file: str):
        V, F = read_off(obj_file)
        return cls(V, F)
    

    def distance_2(self, other: 'object2'):
        N = len(self.fv)
        d2 = 0
        for i in range(N):
            d2 += (self.fv[i] - other.fv[i])**2
        d2 = math.sqrt(d2)
        return d2



    # plotting
    # visualisierungsfunktionen, welche jeden zwischenschritt visualisieren könnnen
    def plot_mesh_V(self, color: str='yellow'):
        x: list[float] = []
        y: list[float] = []
        z: list[float] = []
        for i in self.V:
            x.append(i.x)
            y.append(i.y)
            z.append(i.z)
        ipv.plot_trisurf(x,y,z, triangles=self.F, color=color) # type: ignore

    def plot_mesh_V1(self, color: str='yellow'):
        x: list[float] = []
        y: list[float] = []
        z: list[float] = []
        for i in self.V1:
            x.append(i.x)
            y.append(i.y)
            z.append(i.z)
        ipv.plot_trisurf(x,y,z, triangles=self.F, color=color) # type: ignore
    
    def plot_mesh_V2(self, color: str='yellow'):
        x: list[float] = []
        y: list[float] = []
        z: list[float] = []
        for i in self.V2:
            x.append(i.x)
            y.append(i.y)
            z.append(i.z)
        ipv.plot_trisurf(x,y,z, triangles=self.F, color=color) # type: ignore

    def plot_mesh_V3(self, color: str='yellow'):
        x: list[float] = []
        y: list[float] = []
        z: list[float] = []
        for i in self.V3:
            x.append(i.x)
            y.append(i.y)
            z.append(i.z)
        ipv.plot_trisurf(x,y,z, triangles=self.F, color=color) # type: ignore

    def plot_X_v3(self, color: str='red'):
        x: list[float] = []
        y: list[float] = []
        z: list[float] = []
        for i in self.X:
            x.append(i.x)
            y.append(i.y)
            z.append(i.z)
        x = np.array(x)    # type: ignore
        y = np.array(y)    # type: ignore
        z = np.array(z)    # type: ignore
        line = ipv.plot(x, y, z, color=color) # type: ignore

    def plot_U_v3(self, color: str='red'):
        x: list[float] = []
        y: list[float] = []
        z: list[float] = []
        for i in self.U:
            x.append(i.x)
            y.append(i.y)
            z.append(i.z)
        x = np.array(x) * object2.plot_scale_U # type: ignore
        y = np.array(y) * object2.plot_scale_U # type: ignore
        z = np.array(z) * object2.plot_scale_U # type: ignore
        line = ipv.plot(x, y, z, color=color) # type: ignore

    def scatter_U_v3(self, color: str='red'):
        x: list[float] = []
        y: list[float] = []
        z: list[float] = []
        for i in self.U:
            x.append(i.x)
            y.append(i.y)
            z.append(i.z)
        x = np.array(x) * object2.plot_scale_U # type: ignore
        y = np.array(y) * object2.plot_scale_U # type: ignore
        z = np.array(z) * object2.plot_scale_U # type: ignore
        ipv.scatter(x, y, z, color=color) # type: ignore

    def scatter_X_v3(self, color:str='red'):
        x: list[float] = []
        y: list[float] = []
        z: list[float] = []
        for i in self.X:
            x.append(i.x)
            y.append(i.y)
            z.append(i.z)
        x = np.array(x)    # type: ignore
        y = np.array(y)    # type: ignore
        z = np.array(z)    # type: ignore
        ipv.scatter(x, y, z, color=color) # type: ignore

    def plot_R(self):
        N = len(self.R)
        t = [(2*np.pi)*i/N for i in range(N)]
        plt.plot(t,self.R) # type: ignore
    def plot_R_real(self):
        N = len(self.R_real)
        t = [(2*np.pi)*i/N for i in range(N)]
        plt.plot(t,self.R_real) # type: ignore
