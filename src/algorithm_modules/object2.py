from src.algorithm_modules.model_descriptor.curve import compute_spherical_helix, compute_X_and_R_from_T_devided_v3
from src.algorithm_modules.model_descriptor.cPCA import center_vertices, sort_vertices_by_triangle_T, compute_covariance_matrix_cI,compute_eigs, align_centered_vertices, compute_all_mesh_info, compute_flipping_vector, compute_scaling_factor, scale_and_flipp_normalized_mesh
from src.algorithm_modules.model_descriptor.feature_vector import extract_feature_vector
from src.algorithm_modules.model_descriptor.fourier import compute_fourier_coefficients, invert_FSC_v3
from src.algorithm_modules.utils.parsing import read_obj_file, read_off_file
from src.algorithm_modules.data_structure.vector3 import Vector3
import matplotlib.pyplot as plt
import numpy as np
import math
import ipyvolume as ipv
# from sre


class object2: # dtype vec3
    # number_of_points = 15000 # Anzahl Punkte auf der 3D-Kurve
    # winding_speed = 200 # Windungszahl
    # p_min = 64000 # wird für die bestimmung des Skalierungsfaktors verwendet
    # c_number = 300 # Bestimmt Anzahl Fourier-Koeffizienen im Merkmalsvektor
    plot_scale_U = 5 # skalierung für die visualisierung
    # U = compute_U_v3(number_of_points, winding_speed)
    def __init__(self, V: list[Vector3], F: list[tuple[int, int, int]], number_of_points: int, winding_speed: int, p_min:int, c_number: int):
        self.V = V
        self.F = F
        self.number_of_points = number_of_points
        self.winding_speed = winding_speed
        self.p_min = p_min
        self.c_number = c_number

        self.U = compute_spherical_helix(self.number_of_points, self.winding_speed)
        # normalisierung
        self.T, self.S, self.S_total, self.G, self.m_I, self.normals1  = compute_all_mesh_info(self.V, self.F)
        self.V1 = center_vertices(self.V, self.m_I)
        self.T1 = sort_vertices_by_triangle_T(self.V1, self.F)
        self.G1 = center_vertices(self.G, self.m_I)
        self.C_I = compute_covariance_matrix_cI(self.S, self.S_total, self.G1, self.T1)
        self.eig_values, self.A = compute_eigs(self.C_I)
        self.V2 = align_centered_vertices(self.V1, self.A)
        self.T2 = sort_vertices_by_triangle_T(self.V2, self.F)
        self.Fl = compute_flipping_vector(self.T2, self.S, self.S_total)
        self.scale = compute_scaling_factor(self.T2, self.S, self.S_total, self.p_min)
        self.V3 = scale_and_flipp_normalized_mesh(self.V2, self.Fl, self.scale)

        # extrahierung des Merkmalsvektors fv
        self.X, self.R = compute_X_and_R_from_T_devided_v3(self.U, self.V3, self.F)
        (self.As, self.Bs), self.Cs = compute_fourier_coefficients(self.c_number, self.R)
        self.R_real = invert_FSC_v3(self.number_of_points, (self.As, self.Bs))
        self.fv = extract_feature_vector(self.Cs)


    # Polygonnetze können aus OBJ oder OFF gelesen werden
    @classmethod
    def from_obj(cls, obj_file: str,  number_of_points: int, winding_speed: int, p_min:int, c_number: int):
        V, F = read_obj_file(obj_file)
        return cls(V, F,  number_of_points, winding_speed, p_min, c_number)
    @classmethod
    def from_off(cls, obj_file: str,  number_of_points: int, winding_speed: int, p_min:int, c_number: int):
        V, F = read_off_file(obj_file)
        return cls(V, F,  number_of_points, winding_speed, p_min, c_number)
    

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
