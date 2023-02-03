from src.algorithm_modules.data_structure.vector3 import Vector3
from src.algorithm_modules.data_structure.matrix3 import Matrix3
import numpy.linalg as npl
import numpy as np
import math

def sort_vertices_by_triangle_T(vertices_V: list[Vector3], faces_F: list[tuple[int, int, int]]) -> list[Vector3]:
    vertices_sorted_by_triangle: list[Vector3] = [] # Achtung: Eckpunkte werden mehrmals aufgeführt
    for face in faces_F:
        vertex_1_index, vertex_2_index, vertex_3_index = face
        vertices_sorted_by_triangle.append(vertices_V[vertex_1_index])
        vertices_sorted_by_triangle.append(vertices_V[vertex_2_index])
        vertices_sorted_by_triangle.append(vertices_V[vertex_3_index])
    return vertices_sorted_by_triangle

def calculate_total_and_triangles_surfaces_S(vertices_sorted_by_triangle_T: list[Vector3]) -> tuple[list[float], float]:
    total_mesh_surface_S = 0
    triangles_surfaces_S: list[float] = []
    n = int(len(vertices_sorted_by_triangle_T) /3)
    for i in range(n):
        ii = 3 * i
        v_0 = vertices_sorted_by_triangle_T[ii + 0]
        v_1 = vertices_sorted_by_triangle_T[ii + 1]
        v_2 = vertices_sorted_by_triangle_T[ii + 2]
        normal = v_2.sub(v_0).cross(v_1.sub(v_0))
        s = normal.length() * 0.5
        total_mesh_surface_S += s
        triangles_surfaces_S.append(s)
    return triangles_surfaces_S, total_mesh_surface_S

def calculate_center_of_gravity_of_all_triangles_G(vertices_sorted_by_triangle_T: list[Vector3]) -> list[Vector3]:
    triangles_centers_of_gravity_G: list[Vector3] = []
    n = int(len(vertices_sorted_by_triangle_T) /3)
    
    for i in range(n):
        ii = 3 * i
        v_0 = vertices_sorted_by_triangle_T[ii + 0]
        v_1 = vertices_sorted_by_triangle_T[ii + 1]
        v_2 = vertices_sorted_by_triangle_T[ii + 2]
        c_x = (v_0.x + v_1.x + v_2.x) / 3
        c_y = (v_0.y + v_1.y + v_2.y) / 3
        c_z = (v_0.z + v_1.z + v_2.z) / 3
        triangles_centers_of_gravity_G.append(Vector3(c_x, c_y, c_z))
    return triangles_centers_of_gravity_G

def calculate_mesh_center_of_gravity_mI(triangles_surfaces_S: list[float], total_mesh_surface_S: float, triangles_centers_of_gravity_G: list[Vector3]) -> Vector3:
    mesh_center_of_gravity_mI = Vector3(0, 0, 0)
    for i in range(len(triangles_surfaces_S)):
        mesh_center_of_gravity_mI.add_to_self(triangles_centers_of_gravity_G[i].multiply_by_scalar(triangles_surfaces_S[i]))
    mesh_center_of_gravity_mI = mesh_center_of_gravity_mI.multiply_by_scalar(1/total_mesh_surface_S)
    return mesh_center_of_gravity_mI


def compute_all_mesh_info(vertices_V: list[Vector3], faces_F: list[tuple[int, int, int]]) -> tuple[list[Vector3], list[float], float, list[Vector3], Vector3, list[Vector3]]:
    # die oberen 4 Funktionen werden kombiniert, um Anzahl Iterationen zu verringern
    vertices_sorted_by_triangle: list[Vector3] = []
    total_mesh_surface = 0
    triangles_surfaces: list[float] = []
    triangles_centers_of_gravity: list[Vector3] = []
    mesh_center_of_gravity_mI = Vector3(0, 0, 0)
    normals: list[Vector3] = []
    for i in range(len(faces_F)):
        f1, f2, f3 = faces_F[i]
        v_0, v_1, v_2 = vertices_V[f1], vertices_V[f2], vertices_V[f3]
        vertices_sorted_by_triangle.append(v_0)
        vertices_sorted_by_triangle.append(v_1)
        vertices_sorted_by_triangle.append(v_2)

        normal = v_2.sub(v_0).cross(v_1.sub(v_0))
        normals.append(normal)
        s = normal.length() * 0.5
        total_mesh_surface += s
        triangles_surfaces.append(s)

        c_x = (v_0.x + v_1.x + v_2.x) / 3
        c_y = (v_0.y + v_1.y + v_2.y) / 3
        c_z = (v_0.z + v_1.z + v_2.z) / 3
        g = Vector3(c_x, c_y, c_z)
        triangles_centers_of_gravity.append(g)

        mesh_center_of_gravity_mI.add_to_self(triangles_centers_of_gravity[i].multiply_by_scalar(s))
    mesh_center_of_gravity_mI = mesh_center_of_gravity_mI.multiply_by_scalar(1/total_mesh_surface)
    return vertices_sorted_by_triangle, triangles_surfaces, total_mesh_surface, triangles_centers_of_gravity, mesh_center_of_gravity_mI, normals
    
def center_vertices(vertices_V: list[Vector3], mesh_center_of_gravity_mI: Vector3) -> list[Vector3]:
    centered_vertices_V1: list[Vector3] = []
    for vertex in vertices_V:
        centered_vertices_V1.append(vertex.sub(mesh_center_of_gravity_mI))
    return centered_vertices_V1

def compute_covariance_matrix_cI(triangle_surfaces_S: list[float], total_mesh_surface_S: float, centered_triangles_centers_of_gravity_G1: list[Vector3], centered_sorted_vertices_by_triangle_T1:list[Vector3]) -> Matrix3:
    n = int(len(centered_sorted_vertices_by_triangle_T1) /3)
    covariance_matrix_cI = Matrix3(
        0,0,0,
        0,0,0,
        0,0,0
    )
    for i in range(n):
        ii = 3 * i
        v_0 = centered_sorted_vertices_by_triangle_T1[ii + 0]
        v_1 = centered_sorted_vertices_by_triangle_T1[ii + 1]
        v_2 = centered_sorted_vertices_by_triangle_T1[ii + 2]
        g = centered_triangles_centers_of_gravity_G1[i]
        c = Vector3.covariance_matrix(g, g).multiply_by_scalar(9)
        c.add_to_self(Vector3.covariance_matrix(v_0, v_0))
        c.add_to_self(Vector3.covariance_matrix(v_1, v_1))
        c.add_to_self(Vector3.covariance_matrix(v_2, v_2))
        covariance_matrix_cI.add_to_self(c.multiply_by_scalar(triangle_surfaces_S[i]))
    covariance_matrix_cI = covariance_matrix_cI.multiply_by_scalar(1/(12 * total_mesh_surface_S))
    return covariance_matrix_cI

def compute_eigs(c_I_1: Matrix3) -> tuple[Vector3, Matrix3]:
    c_I = c_I_1.to_array()
    eig_values, eig_vectors = npl.eig(c_I)
    
    sorted_indices = np.argsort(eig_values)
    eig_vec_T = eig_vectors.T 
    transformation_matrix_A = np.zeros((3,3))
    sorted_eig_values = np.zeros((1,3))[0]
    for i in range(len(transformation_matrix_A)):
        ii = sorted_indices[2-i]
        transformation_matrix_A[i] = eig_vec_T[ii] 
        sorted_eig_values[i] = eig_values[ii]
    eigs = Vector3.from_array(sorted_eig_values), Matrix3.from_array(transformation_matrix_A)
    return eigs

def align_centered_vertices(centered_vertices_V1: list[Vector3], transformation_matrix_A: Matrix3) -> list[Vector3]:
    aligned_centered_vertices_V2: list[Vector3] = []
    for v in centered_vertices_V1:
        v2 = v.right_multiply_by_matrix3(transformation_matrix_A)
        aligned_centered_vertices_V2.append(v2)
    return aligned_centered_vertices_V2

    
def compute_flipping_vector(aligned_centered_vertices_sorted_by_triangle_T2: list[Vector3], triangle_surfaces_S: list[float], total_mesh_surface_S: float) -> Vector3:
    n = int(len(aligned_centered_vertices_sorted_by_triangle_T2) / 3)
    fx = 0
    fy = 0
    fz = 0
    Fxyz: list[float] = [0, 0, 0]
    for i in range(n):
        s = triangle_surfaces_S[i]
        ii = i * 3
        v_0 = aligned_centered_vertices_sorted_by_triangle_T2[ii + 0]
        v_1 = aligned_centered_vertices_sorted_by_triangle_T2[ii + 1]
        v_2 = aligned_centered_vertices_sorted_by_triangle_T2[ii + 2]
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
    fx /= 6*total_mesh_surface_S
    fy /= 6*total_mesh_surface_S
    fz /= 6*total_mesh_surface_S
    sign_x = math.copysign(1, fx)
    sign_y = math.copysign(1, fy)
    sign_z = math.copysign(1, fz)
    flipping_vector_Fl = Vector3(sign_x, sign_y, sign_z)
    return flipping_vector_Fl

def compute_scaling_factor(aligned_centered_vertices_sorted_by_triangle_T2: list[Vector3], triangle_surfaces_S: list[float], total_mesh_surface_S: float, number_of_points_to_approximate_mesh_surface_p_min: int) -> float:
    n = int(len(aligned_centered_vertices_sorted_by_triangle_T2) / 3)
    scaling_factor = 0
    for i in range(n):
        s = triangle_surfaces_S[i]
        if s == 0:
            p_j = 1
        else:
            s = triangle_surfaces_S[i]
            p_j = int(math.ceil(math.sqrt(number_of_points_to_approximate_mesh_surface_p_min*s/total_mesh_surface_S)))
        ii = i * 3
        a = aligned_centered_vertices_sorted_by_triangle_T2[ii + 0]
        b = aligned_centered_vertices_sorted_by_triangle_T2[ii + 1]
        c = aligned_centered_vertices_sorted_by_triangle_T2[ii + 2]
        denom = 1/p_j
        d_ab = (b.sub(a)).multiply_by_scalar(denom)
        d_ac = (c.sub(a)).multiply_by_scalar(denom)
        d_g = (d_ab.add(d_ac)).multiply_by_scalar(1/3)
        gamma = s / ((p_j)**2)
        for x in range(p_j - 1):
            for y in range(x+1):
                g = a.add(d_ab.multiply_by_scalar((x-y)).add(d_ac.multiply_by_scalar(y).add(d_g)))
                scaling_factor += gamma*(g.length() + (g.add(d_g)).length())
        for y in range(p_j):
            g = a.add(d_ab.multiply_by_scalar(p_j-1-y).add(d_ac.multiply_by_scalar(y).add(d_g)))
            scaling_factor += gamma*g.length()
    scaling_factor *= 1/total_mesh_surface_S
    return scaling_factor


def scale_and_flipp_normalized_mesh(shifted_and_aligned_vertices: list[Vector3], flipping_vector: Vector3, scaling_factor: float) -> list[Vector3]: # V2 wird skaliert und eventuel reklektiert --> V3
    normalzied_vertices: list[Vector3] = []
    inv_scale = 1 / scaling_factor
    for v in shifted_and_aligned_vertices:
        normalized_vertex = v.multiply_by_vec3(flipping_vector).multiply_by_scalar(inv_scale)
        normalzied_vertices.append(normalized_vertex)
    return normalzied_vertices
