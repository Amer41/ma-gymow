from src.algorithm_modules.data_structure.triangle import Triangle
from src.algorithm_modules.data_structure.vector3 import Vector3
from typing import Optional



def compute_triangle_list(vertices: list[Vector3], faces: list[tuple[int, int, int]]) -> list[Triangle]:
    triangles: list[Triangle] = []
    for face in faces:
        vertex_1_index, vertex_2_index, vertex_3_index = face
        triangle = Triangle(vertices[vertex_1_index],vertices[vertex_2_index],vertices[vertex_3_index])
        triangles.append(triangle)
    return triangles

def segment_triangle_intersection(segment: Vector3, triangle: Triangle) -> Optional[Vector3]:

    d = segment
    denom = d.dot(triangle.normal_vector)
    if denom == 0:
        # Schnittpunkte auf der anderen Seite vom Ursprung werden nicht beachtet (negative Abstände einführen?)
        return None
    inv_denom = 1.0 / denom
    u = d.dot(triangle.u_constant) * inv_denom
    if u > 1 or u < 0:
        return None
    v = d.dot(triangle.v_constant) * inv_denom
    if u + v > 1 or v < 0:
        return None
    t = triangle.t_contsant * inv_denom
    if t < 0:
        return None
    else:
        return d.multiply_by_scalar(t)