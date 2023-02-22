from math import pi, sqrt, sin, cos
from src.algorithm_modules.data_structure.vector3 import Vector3
from src.algorithm_modules.model_descriptor.aabb import AABB
"""
    algorihtm src: https://www.cmu.edu/biolphys/deserno/pdf/sphere_equi.pdf

"""
def create_point_on_sphere(polar_angle_upsilon: float, azimuthal_angle_phi: float) -> Vector3:
    z_coordinate = sin(polar_angle_upsilon) * cos(azimuthal_angle_phi)
    y_coordinate = sin(polar_angle_upsilon) * sin(azimuthal_angle_phi)
    x_coordinate = cos(polar_angle_upsilon)
    return Vector3(x_coordinate, y_coordinate, z_coordinate)


def generate_sphere_with_equidistibuted_points(number_of_points: int, radius: float = 1) -> list[Vector3]:
    equidistributed_points_on_sphere: list[Vector3] = []
    interval_of_circles_of_latitude_d_upsilon = ...
    interval_of_points_d_phi = ...
    N_count = 0
    sphere_surface = pi * 4 * (radius)**2
    surface_per_point = sphere_surface/number_of_points
    d = sqrt(surface_per_point)
    number_of_circles_of_latitude_M_upsilon = round(pi/d)
    interval_of_circles_of_latitude_d_upsilon = pi/number_of_circles_of_latitude_M_upsilon
    interval_of_points_d_phi = surface_per_point/interval_of_circles_of_latitude_d_upsilon

    for circle_of_latitude in range(number_of_circles_of_latitude_M_upsilon):
        polar_angle_upsilon = pi * (circle_of_latitude + 0.5) / number_of_circles_of_latitude_M_upsilon
        number_of_points_on_circle_M_phi = round((2 * pi * sin(polar_angle_upsilon)) / interval_of_points_d_phi)
        for point in range(number_of_points_on_circle_M_phi):
            azimuthal_angle_phi = (2 * pi * point) / number_of_points_on_circle_M_phi
            equidistributed_points_on_sphere.append(create_point_on_sphere(polar_angle_upsilon, azimuthal_angle_phi))
            N_count += 1
    # print(N_count)
    # print(number_of_circles_of_latitude_M_upsilon)
    return equidistributed_points_on_sphere


def stretch_equi_sphere_using_eigs(eigen_values: Vector3, sphere: list[Vector3]):
    stretched_sphere: list[Vector3] = []
    for point in sphere:
        stretched_sphere.append(eigen_values.multiply_by_vec3(point))
    return stretched_sphere

def stretch_equi_sphere_using_aabb(aabb: AABB, sphere: list[Vector3]):
    for point in sphere:
        if point.x >= 0:
            point.scale_x(abs(aabb.x_range.max))
        else:
            point.scale_x(abs(aabb.x_range.min))

        if point.y >= 0:
            point.scale_y(abs(aabb.y_range.max))
        else:
            point.scale_y(abs(aabb.y_range.min))

        if point.z >= 0:
            point.scale_z(abs(aabb.z_range.max))
        else:
            point.scale_z(abs(aabb.z_range.min))      

def compute_spherical_helix(number_of_points: int, winding_speed: int) -> list[Vector3]:
    n = number_of_points 
    time: list[float] = [pi*i*(1/(n)) for i in range(n)]
    q = winding_speed
    denom = n - 1
    spherical_helix: list[Vector3] = []
    for t in time:
        x = cos(t*(n/(denom)))
        y = sin(q*t*(n/(denom)))*sin(t*(n/(denom)))
        z = cos(q*t*(n/(denom)))*sin(t*(n/(denom)))
        spherical_helix.append(Vector3(x,y,z))
    return spherical_helix

