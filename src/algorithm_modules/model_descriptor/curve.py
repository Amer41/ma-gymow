import math
from src.algorithm_modules.data_structure.vector3 import Vector3
from src.algorithm_modules.data_structure.triangle import Triangle
from src.algorithm_modules.model_descriptor.mt_intersection_algorithm import segment_triangle_intersection, compute_triangle_list


def compute_spherical_helix(number_of_points: int, winding_speed: int) -> list[Vector3]:
    n = number_of_points 
    time: list[float] = [math.pi*i*(1/(n)) for i in range(n)]
    q = winding_speed
    denom = n - 1
    spherical_helix: list[Vector3] = []
    for t in time:
        x = math.cos(t*(n/(denom)))
        y = math.sin(q*t*(n/(denom)))*math.sin(t*(n/(denom)))
        z = math.cos(q*t*(n/(denom)))*math.sin(t*(n/(denom)))
        spherical_helix.append(Vector3(x,y,z))
    return spherical_helix

def takesecond(elem):
    # dient für die Sortierung von Listen (Sortierung nach dem 2. Element ihrer Mitglieder)
    return elem[1]

def devide_triangle_list(triangles: list[Triangle]) -> list[list[Triangle]]:
    T111: list[Triangle] = [] # +++ (Vorzeichen von xyz)
    T11_1: list[Triangle] = [] # ++-
    T1_11: list[Triangle] = [] # +-+
    T1_1_1: list[Triangle] = [] # ...
    T_111: list[Triangle] = []
    T_11_1: list[Triangle] = []
    T_1_11: list[Triangle] = []
    T_1_1_1: list[Triangle] = []
    for i in range(len(triangles)):
        triangle = triangles[i]
        triangle_T = [triangle.x_coordinate_of_vertices, triangle.y_coordinate_of_vertices, triangle.z_coordinate_of_vertices]
        if all(n >= 0 for n in triangle_T[0]): # +
                                if all(n >= 0 for n in triangle_T[1]): # +
                                                        if all(n >= 0 for n in triangle_T[2]): # +
                                                            T111.append(triangle)
                                                        elif all(n < 0 for n in triangle_T[2]): #-
                                                            T11_1.append(triangle)
                                                        else: # + und -
                                                            T111.append(triangle)
                                                            T11_1.append(triangle)
                                elif all(n < 0 for n in triangle_T[1]): #-
                                                        if all(n >= 0 for n in triangle_T[2]): # +
                                                            T1_11.append(triangle)
                                                        elif all(n < 0 for n in triangle_T[2]): #-
                                                            T1_1_1.append(triangle)
                                                        else: # + und -
                                                            T1_11.append(triangle)
                                                            T1_1_1.append(triangle)
                                else: # + und -
                                                        if all(n >= 0 for n in triangle_T[2]): # +
                                                            T111.append(triangle)
                                                            T1_11.append(triangle)
                                                        elif all(n < 0 for n in triangle_T[2]): #-
                                                            T11_1.append(triangle)
                                                            T1_1_1.append(triangle)
                                                        else: # + und - (*)
                                                            T111.append(triangle)
                                                            T1_11.append(triangle)
                                                            T11_1.append(triangle)
                                                            T1_1_1.append(triangle)
        elif all(n < 0 for n in triangle_T[0]): #-
                                if all(n >= 0 for n in triangle_T[1]): # +
                                                        if all(n >= 0 for n in triangle_T[2]): # +
                                                            T_111.append(triangle)
                                                        elif all(n < 0 for n in triangle_T[2]): #-
                                                            T_11_1.append(triangle)
                                                        else: # + und -
                                                            T_111.append(triangle)
                                                            T_11_1.append(triangle)
                                elif all(n < 0 for n in triangle_T[1]): #-
                                                        if all(n >= 0 for n in triangle_T[2]): # +
                                                            T_1_11.append(triangle)
                                                        elif all(n < 0 for n in triangle_T[2]): #-
                                                            T_1_1_1.append(triangle)
                                                        else: # + und -
                                                            T_1_11.append(triangle)
                                                            T_1_1_1.append(triangle)
                                else: # + und -
                                                        if all(n >= 0 for n in triangle_T[2]): # +
                                                            T_111.append(triangle)
                                                            T_1_11.append(triangle)
                                                        elif all(n < 0 for n in triangle_T[2]): #-
                                                            T_11_1.append(triangle)
                                                            T_1_1_1.append(triangle)
                                                        else: # + und - (*)
                                                            T_111.append(triangle)
                                                            T_1_11.append(triangle)
                                                            T_11_1.append(triangle)
                                                            T_1_1_1.append(triangle)
        else: # + und -
                                if all(n >= 0 for n in triangle_T[1]): # +
                                                        if all(n >= 0 for n in triangle_T[2]): # +
                                                            T111.append(triangle)
                                                            T_111.append(triangle)
                                                        elif all(n < 0 for n in triangle_T[2]): #-
                                                            T11_1.append(triangle)
                                                            T_11_1.append(triangle)
                                                        else: # + und - (*)
                                                            T111.append(triangle)
                                                            T11_1.append(triangle)
                                                            T_111.append(triangle)
                                                            T_11_1.append(triangle)
                                elif all(n < 0 for n in triangle_T[1]): #-
                                                        if all(n >= 0 for n in triangle_T[2]): # +
                                                            T1_11.append(triangle)
                                                            T_1_11.append(triangle)
                                                        elif all(n < 0 for n in triangle_T[2]): #-
                                                            T1_1_1.append(triangle)
                                                            T_1_1_1.append(triangle)
                                                        else: # + und - (*)
                                                            T1_11.append(triangle)
                                                            T1_1_1.append(triangle)
                                                            T_1_11.append(triangle)
                                                            T_1_1_1.append(triangle)
                                else: # + und -
                                                        if all(n >= 0 for n in triangle_T[2]): # + (*)
                                                            T111.append(triangle)
                                                            T1_11.append(triangle)
                                                            T_111.append(triangle)
                                                            T_1_11.append(triangle)
                                                        elif all(n < 0 for n in triangle_T[2]): #- (*)
                                                            T11_1.append(triangle)
                                                            T1_1_1.append(triangle)
                                                            T_11_1.append(triangle)
                                                            T_1_1_1.append(triangle)
                                                        else: # + und - (*) eigentlich ummöglich in 8
                                                            T111.append(triangle)
                                                            T1_11.append(triangle)
                                                            T_111.append(triangle)
                                                            T_1_11.append(triangle)
                                                            T11_1.append(triangle)
                                                            T1_1_1.append(triangle)
                                                            T_11_1.append(triangle)
                                                            T_1_1_1.append(triangle)
    devided_triangle_list = [
        T111,
        T11_1,
        T1_11,
        T1_1_1,
        T_111,
        T_11_1,
        T_1_11,
        T_1_1_1
    ]
    return devided_triangle_list


def compute_3D_curve_X_and_its_distance_from_origin_R(spherical_curve: list[Vector3], vertices: list[Vector3], faces: list[tuple[int, int, int]]) -> tuple[list[Vector3], list[float]]:
    triangles = compute_triangle_list(vertices, faces)
    devided_triangle_list = devide_triangle_list(triangles)
    n = len(spherical_curve) 
    distances: list[float] = []
    intersection_points: list[Vector3] = []
    for i in range(n):
        intersection_points_and_distances: list[tuple[Vector3, float]] = []
        if spherical_curve[i].x >= 0:
                        if spherical_curve[i].y >= 0:
                                        if spherical_curve[i].z >= 0:
                                            # print('111')
                                            for t in devided_triangle_list[0]:
                                                q = segment_triangle_intersection(spherical_curve[i], t)
                                                if q:
                                                    r = q.length()
                                                    intersection_points_and_distances.append((q, r))
                                        elif spherical_curve[i].z < 0:
                                            # print('11_1')
                                            for t in devided_triangle_list[1]:
                                                q = segment_triangle_intersection(spherical_curve[i], t)
                                                if q:
                                                    r = q.length()
                                                    intersection_points_and_distances.append((q, r))
                                        else:
                                            print('Fehler 2')
                        elif spherical_curve[i].y < 0:
                                        if spherical_curve[i].z >= 0:
                                            # print('1_11')
                                            for t in devided_triangle_list[2]:
                                                q = segment_triangle_intersection(spherical_curve[i], t)
                                                if q:
                                                    r = q.length()
                                                    intersection_points_and_distances.append((q, r))
                                        elif spherical_curve[i].z < 0:
                                            # print('1_1_1')
                                            for t in devided_triangle_list[3]:
                                                q = segment_triangle_intersection(spherical_curve[i], t)
                                                if q:
                                                    r = q.length()
                                                    intersection_points_and_distances.append((q, r))
                                        else:
                                            print('Fehler 3')
                        else:
                            print('Fehler 1')
        elif spherical_curve[i].x < 0:
                        if spherical_curve[i].y >= 0:
                                        if spherical_curve[i].z >= 0:
                                            # print('_111')
                                            for t in devided_triangle_list[4]:
                                                q = segment_triangle_intersection(spherical_curve[i], t)
                                                if q:
                                                    r = q.length()
                                                    intersection_points_and_distances.append((q, r))

                                        elif spherical_curve[i].z < 0:
                                            # print('_11_1')
                                            for t in devided_triangle_list[5]:
                                                q = segment_triangle_intersection(spherical_curve[i], t)
                                                if q:
                                                    r = q.length()
                                                    intersection_points_and_distances.append((q, r))
                                        else:
                                            print('Fehler 5')
                        elif spherical_curve[i].y < 0:
                                        if spherical_curve[i].z >= 0:
                                            # print('_1_11')
                                            for t in devided_triangle_list[6]:
                                                q = segment_triangle_intersection(spherical_curve[i], t)
                                                if q:
                                                    r = q.length()
                                                    intersection_points_and_distances.append((q, r))
                                        elif spherical_curve[i].z < 0:  
                                            # print('_1_1_1')
                                            for t in devided_triangle_list[7]:
                                                q = segment_triangle_intersection(spherical_curve[i], t)
                                                if q:
                                                    r = q.length()
                                                    intersection_points_and_distances.append((q, r))
                                        else:
                                            print('Fehler 6')

                        else:
                            print('Fehler 4')
        else:
            print('Fehler')
        if len(intersection_points_and_distances) == False:
            intersection_points_and_distances.append((Vector3(0,0,0), 0))
        else:
            intersection_points_and_distances.sort(key=takesecond, reverse=True)
        intersection_points.append(intersection_points_and_distances[0][0])
        distances.append(intersection_points_and_distances[0][1])
    return intersection_points, distances


