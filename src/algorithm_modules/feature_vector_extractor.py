from src.algorithm_modules.model_descriptor.curve import compute_spherical_helix, compute_3D_curve_X_and_its_distance_from_origin_R
from src.algorithm_modules.model_descriptor.cPCA import center_vertices, sort_vertices_by_triangle_T, compute_covariance_matrix_cI,compute_eigs, align_centered_vertices, compute_all_mesh_info, compute_flipping_vector, compute_scaling_factor, scale_and_flipp_normalized_mesh
from src.algorithm_modules.model_descriptor.feature_vector import extract_feature_vector
from src.algorithm_modules.model_descriptor.fourier import compute_fourier_coefficients, invert_FSC
from src.algorithm_modules.utils.parsing import read_obj_file, read_off_file
from src.algorithm_modules.data_structure.vector3 import Vector3
import matplotlib.pyplot as plt
import numpy as np
import math
import ipyvolume as ipv


class FeatureVectorExtractor:
    '''
    number_of_points: Anzahl Punkte auf der 3D-Kurve
    winding_speed: Windungszahl der 3D-Kurve
    p_min: wird für die bestimmung des Skalierungsfaktors verwendet
    c_number: Bestimmt die Anzahl der Fourier-Koeffizienen im Merkmalsvektor
    '''
    def __init__(self, V: list[Vector3], F: list[tuple[int, int, int]], number_of_points: int, winding_speed: int, p_min:int, c_number: int):
        self.V = V
        self.F = F
        self.number_of_points = number_of_points
        self.winding_speed = winding_speed
        self.p_min = p_min
        self.c_number = c_number

        self.spherical_helix = compute_spherical_helix(self.number_of_points, self.winding_speed)

        # --------------- normalisierung -------------------

        self.vertices_sorted_by_triangle_T, self.triangles_surfaces_S, self.total_mesh_surface_S, self.triabgles_centers_of_gravity_G, self.mesh_center_of_gravity_mI, self.normal_vectors  = compute_all_mesh_info(self.V, self.F)
        self.centered_vertices_V1 = center_vertices(self.V, self.mesh_center_of_gravity_mI)
        self.centered_vertices_sorted_by_triangle_T1 = sort_vertices_by_triangle_T(self.centered_vertices_V1, self.F)
        self.centered_triangles_centers_of_gravity_G1 = center_vertices(self.triabgles_centers_of_gravity_G, self.mesh_center_of_gravity_mI)
        self.covaraince_matrix_cI = compute_covariance_matrix_cI(self.triangles_surfaces_S, self.total_mesh_surface_S, self.centered_triangles_centers_of_gravity_G1, self.centered_vertices_sorted_by_triangle_T1)
        self.eig_values, self.transformation_matrix_A = compute_eigs(self.covaraince_matrix_cI)
        self.aligned_centered_vertices_V2 = align_centered_vertices(self.centered_vertices_V1, self.transformation_matrix_A)
        self.aligned_centered_vertices_sorted_by_triangle_T2 = sort_vertices_by_triangle_T(self.aligned_centered_vertices_V2, self.F)
        self.flipping_vector_Fl = compute_flipping_vector(self.aligned_centered_vertices_sorted_by_triangle_T2, self.triangles_surfaces_S, self.total_mesh_surface_S)
        self.scaling_factor = compute_scaling_factor(self.aligned_centered_vertices_sorted_by_triangle_T2, self.triangles_surfaces_S, self.total_mesh_surface_S, self.p_min)
        self.normalized_vertices_V3 = scale_and_flipp_normalized_mesh(self.aligned_centered_vertices_V2, self.flipping_vector_Fl, self.scaling_factor)

        # --------------- extrahierung des Merkmalsvektors -------------------

        self._3d_curve_X, self._2d_curve_R = compute_3D_curve_X_and_its_distance_from_origin_R(self.spherical_helix, self.normalized_vertices_V3, self.F)
        (self.As_fourier_coefs, self.Bs_fourier_coefs), self.Cs_fourier_coefs = compute_fourier_coefficients(self.c_number, self._2d_curve_R)
        self.reconstructed_2d_curve_R = invert_FSC(self.number_of_points, (self.As_fourier_coefs, self.Bs_fourier_coefs))
        self.feature_vector = extract_feature_vector(self.Cs_fourier_coefs)


    @classmethod
    def from_obj(cls, obj_file: str,  number_of_points: int, winding_speed: int, p_min:int, c_number: int):
        V, F = read_obj_file(obj_file)
        return cls(V, F,  number_of_points, winding_speed, p_min, c_number)
    @classmethod
    def from_off(cls, obj_file: str,  number_of_points: int, winding_speed: int, p_min:int, c_number: int):
        V, F = read_off_file(obj_file)
        return cls(V, F,  number_of_points, winding_speed, p_min, c_number)
    

    def distance(self, other: 'FeatureVectorExtractor'):
        N = len(self.feature_vector)
        d2 = 0
        for i in range(N):
            d2 += (self.feature_vector[i] - other.feature_vector[i])**2
        d2 = math.sqrt(d2)
        return d2


    # --------------- Visualisierung -------------------
    @staticmethod
    def plot_mesh(vertices: list[Vector3], faces: list[tuple[int, int, int]], color: str='yellow'):
        x: list[float] = []
        y: list[float] = []
        z: list[float] = []
        for i in vertices:
            x.append(i.x)
            y.append(i.y)
            z.append(i.z)
        ipv.plot_trisurf(x,y,z, triangles=faces, color=color)

    @staticmethod
    def plot_3d_curve(curve: list[Vector3], color: str='red'):
        x: list[float] = []
        y: list[float] = []
        z: list[float] = []
        for i in curve:
            x.append(i.x)
            y.append(i.y)
            z.append(i.z)
        x_array = np.array(x)  
        y_array = np.array(y)  
        z_array = np.array(z)  
        line = ipv.plot(x_array, y_array, z_array, color=color)

    @staticmethod
    def scatter_3d(point_set: list[Vector3], plot_scale: float = 1, color: str='red'):
        x: list[float] = []
        y: list[float] = []
        z: list[float] = []
        for i in point_set:
            x.append(i.x)
            y.append(i.y)
            z.append(i.z)
        x_array = np.array(x) * plot_scale
        y_array = np.array(y) * plot_scale
        z_array = np.array(z) * plot_scale
        ipv.scatter(x_array, y_array, z_array, color=color)

    @staticmethod
    def plot_2d_curve_over_time(curve: list[float]):
        N = len(curve)
        t = [(2*np.pi)*i/N for i in range(N)]
        plt.plot(t,curve) 
