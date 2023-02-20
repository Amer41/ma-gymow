from math import pi, sqrt, sin, cos
from src.algorithm_modules.data_structure.vector3 import Vector3
"""
    algorihtm src: https://www.cmu.edu/biolphys/deserno/pdf/sphere_equi.pdf

"""
def create_point_on_sphere(polar_angle_upsilon: float, azimuthal_angle_phi: float) -> Vector3:
    x_coordinate = sin(polar_angle_upsilon) * cos(azimuthal_angle_phi)
    y_coordinate = sin(polar_angle_upsilon) * sin(azimuthal_angle_phi)
    z_coordinate = cos(polar_angle_upsilon)
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

