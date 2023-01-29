import math
from src.modules.vector3 import vec3
from src.modules.triangle import triangle
from typing import Optional


# Die Spirale U wird erstellt
# def compute_U_v3(number_of_points, winding_speed): # Spirale rotiert um z-Achse
#     n = number_of_points 
#     t = [math.pi*i*(1/(n)) for i in range(n)]
#     q = winding_speed
#     denom = n - 1
#     U = []
#     for i in t:
#         x = math.cos(q*i*(n/(denom)))*math.sin(i*(n/(denom)))
#         y = math.sin(q*i*(n/(denom)))*math.sin(i*(n/(denom)))
#         z = math.cos(i*(n/(denom)))
#         U.append(vec3(x,y,z))
#     return U
def compute_U_v3(number_of_points: int, winding_speed: int) -> list[vec3]: # Spirale rotiert um x-Achse
    n = number_of_points 
    t: list[float] = [math.pi*i*(1/(n)) for i in range(n)]
    q = winding_speed
    denom = n - 1
    U: list[vec3] = []
    for i in t:
        z = math.cos(q*i*(n/(denom)))*math.sin(i*(n/(denom)))
        y = math.sin(q*i*(n/(denom)))*math.sin(i*(n/(denom)))
        x = math.cos(i*(n/(denom)))
        U.append(vec3(x,y,z))
    return U

def compute_T3_v3(V3: list[vec3], F: list[tuple[int, int, int]]) -> list[triangle]: # Dreiecke werden in die Klasse Triangle (siehe Oben) eingeführt
    # Das passiert nach der normalisierung
    T: list[triangle] = []
    for f in F:
        f1, f2, f3 = f
        t = triangle(V3[f1],V3[f2],V3[f3])
        T.append(t)
    return T

def takesecond(elem): #type: ignore # dient für die Sortierung von Listen (Sortierung nach dem 2. Element ihrer Mitglieder)
    return elem[1] # type: ignore


def devide_T_v3(T: list[triangle]) -> list[list[triangle]]: # Um Rechenzeit zu reduzieren, werden die Dreiecke in 8 Teilmengen aufgeteilt
    T111: list[triangle] = [] # +++ (Vorzeichen von xyz)
    T11_1: list[triangle] = [] # ++-
    T1_11: list[triangle] = [] # +-+
    T1_1_1: list[triangle] = [] # ...
    T_111: list[triangle] = []
    T_11_1: list[triangle] = []
    T_1_11: list[triangle] = []
    T_1_1_1: list[triangle] = []
    for i in range(len(T)):
        t = T[i]
        t_T = [t.x, t.y, t.z]
        if all(n >= 0 for n in t_T[0]): # +
                                if all(n >= 0 for n in t_T[1]): # +
                                                        if all(n >= 0 for n in t_T[2]): # +
                                                            T111.append(t)
                                                        elif all(n < 0 for n in t_T[2]): #-
                                                            T11_1.append(t)
                                                        else: # + und -
                                                            T111.append(t)
                                                            T11_1.append(t)
                                elif all(n < 0 for n in t_T[1]): #-
                                                        if all(n >= 0 for n in t_T[2]): # +
                                                            T1_11.append(t)
                                                        elif all(n < 0 for n in t_T[2]): #-
                                                            T1_1_1.append(t)
                                                        else: # + und -
                                                            T1_11.append(t)
                                                            T1_1_1.append(t)
                                else: # + und -
                                                        if all(n >= 0 for n in t_T[2]): # +
                                                            T111.append(t)
                                                            T1_11.append(t)
                                                        elif all(n < 0 for n in t_T[2]): #-
                                                            T11_1.append(t)
                                                            T1_1_1.append(t)
                                                        else: # + und - (*)
                                                            T111.append(t)
                                                            T1_11.append(t)
                                                            T11_1.append(t)
                                                            T1_1_1.append(t)
        elif all(n < 0 for n in t_T[0]): #-
                                if all(n >= 0 for n in t_T[1]): # +
                                                        if all(n >= 0 for n in t_T[2]): # +
                                                            T_111.append(t)
                                                        elif all(n < 0 for n in t_T[2]): #-
                                                            T_11_1.append(t)
                                                        else: # + und -
                                                            T_111.append(t)
                                                            T_11_1.append(t)
                                elif all(n < 0 for n in t_T[1]): #-
                                                        if all(n >= 0 for n in t_T[2]): # +
                                                            T_1_11.append(t)
                                                        elif all(n < 0 for n in t_T[2]): #-
                                                            T_1_1_1.append(t)
                                                        else: # + und -
                                                            T_1_11.append(t)
                                                            T_1_1_1.append(t)
                                else: # + und -
                                                        if all(n >= 0 for n in t_T[2]): # +
                                                            T_111.append(t)
                                                            T_1_11.append(t)
                                                        elif all(n < 0 for n in t_T[2]): #-
                                                            T_11_1.append(t)
                                                            T_1_1_1.append(t)
                                                        else: # + und - (*)
                                                            T_111.append(t)
                                                            T_1_11.append(t)
                                                            T_11_1.append(t)
                                                            T_1_1_1.append(t)
        else: # + und -
                                if all(n >= 0 for n in t_T[1]): # +
                                                        if all(n >= 0 for n in t_T[2]): # +
                                                            T111.append(t)
                                                            T_111.append(t)
                                                        elif all(n < 0 for n in t_T[2]): #-
                                                            T11_1.append(t)
                                                            T_11_1.append(t)
                                                        else: # + und - (*)
                                                            T111.append(t)
                                                            T11_1.append(t)
                                                            T_111.append(t)
                                                            T_11_1.append(t)
                                elif all(n < 0 for n in t_T[1]): #-
                                                        if all(n >= 0 for n in t_T[2]): # +
                                                            T1_11.append(t)
                                                            T_1_11.append(t)
                                                        elif all(n < 0 for n in t_T[2]): #-
                                                            T1_1_1.append(t)
                                                            T_1_1_1.append(t)
                                                        else: # + und - (*)
                                                            T1_11.append(t)
                                                            T1_1_1.append(t)
                                                            T_1_11.append(t)
                                                            T_1_1_1.append(t)
                                else: # + und -
                                                        if all(n >= 0 for n in t_T[2]): # + (*)
                                                            T111.append(t)
                                                            T1_11.append(t)
                                                            T_111.append(t)
                                                            T_1_11.append(t)
                                                        elif all(n < 0 for n in t_T[2]): #- (*)
                                                            T11_1.append(t)
                                                            T1_1_1.append(t)
                                                            T_11_1.append(t)
                                                            T_1_1_1.append(t)
                                                        else: # + und - (*) eigentlich ummöglich in 8
                                                            T111.append(t)
                                                            T1_11.append(t)
                                                            T_111.append(t)
                                                            T_1_11.append(t)
                                                            T11_1.append(t)
                                                            T1_1_1.append(t)
                                                            T_11_1.append(t)
                                                            T_1_1_1.append(t)

    T_devided = [
        T111,
        T11_1,
        T1_11,
        T1_1_1,
        T_111,
        T_11_1,
        T_1_11,
        T_1_1_1
    ]
    return T_devided

def intersection_segment_triangle_v3_2(segment: vec3, T: triangle) -> Optional[vec3]: # berchnet schnittpunkt zwischne segment und T, wenn vorhanden
    D = segment
    denom = D.dot(T.normal)
    if denom == 0:
        return None # reicht für unsere Zwecke, kann aber verbessert werden (auf der anderen Seite schauen)
    invDenom = 1.0 / denom
    u = D.dot(T.u_constant) * invDenom
    if u > 1 or u < 0:
        return None
    v = D.dot(T.v_constant) * invDenom
    if u + v > 1 or v < 0:
        return None
    t = T.t * invDenom
    if t < 0:
        return None
    else:
        return D.multiply_scalar(t)

def compute_X_and_R_from_T_devided_v3(U: list[vec3], V3: list[vec3], F: list[tuple[int, int, int]]) -> tuple[list[vec3], list[float]]: # erstellt 3D-Kurve X, und Abstand-Kurve R
    T3 = compute_T3_v3(V3, F)
    T_devided = devide_T_v3(T3)
    n = len(U) 
    R: list[float] = []
    X: list[vec3] = []
    for i in range(n):
        O: list[tuple[vec3, float]] = []
        if U[i].x >= 0:
                        if U[i].y >= 0:
                                        if U[i].z >= 0:
                                            # print('111')
                                            for t in T_devided[0]:
                                                q = intersection_segment_triangle_v3_2(U[i], t)
                                                if q:
                                                    r = q.length()
                                                    O.append((q, r))
                                        elif U[i].z < 0:
                                            # print('11_1')
                                            for t in T_devided[1]:
                                                q = intersection_segment_triangle_v3_2(U[i], t)
                                                if q:
                                                    r = q.length()
                                                    O.append((q, r))
                                        else:
                                            print('Fehler 2')
                        elif U[i].y < 0:
                                        if U[i].z >= 0:
                                            # print('1_11')
                                            for t in T_devided[2]:
                                                q = intersection_segment_triangle_v3_2(U[i], t)
                                                if q:
                                                    r = q.length()
                                                    O.append((q, r))
                                        elif U[i].z < 0:
                                            # print('1_1_1')
                                            for t in T_devided[3]:
                                                q = intersection_segment_triangle_v3_2(U[i], t)
                                                if q:
                                                    r = q.length()
                                                    O.append((q, r))
                                        else:
                                            print('Fehler 3')
                        else:
                            print('Fehler 1')
        elif U[i].x < 0:
                        if U[i].y >= 0:
                                        if U[i].z >= 0:
                                            # print('_111')
                                            for t in T_devided[4]:
                                                q = intersection_segment_triangle_v3_2(U[i], t)
                                                if q:
                                                    r = q.length()
                                                    O.append((q, r))

                                        elif U[i].z < 0:
                                            # print('_11_1')
                                            for t in T_devided[5]:
                                                q = intersection_segment_triangle_v3_2(U[i], t)
                                                if q:
                                                    r = q.length()
                                                    O.append((q, r))
                                        else:
                                            print('Fehler 5')
                        elif U[i].y < 0:
                                        if U[i].z >= 0:
                                            # print('_1_11')
                                            for t in T_devided[6]:
                                                q = intersection_segment_triangle_v3_2(U[i], t)
                                                if q:
                                                    r = q.length()
                                                    O.append((q, r))
                                        elif U[i].z < 0:  
                                            # print('_1_1_1')
                                            for t in T_devided[7]:
                                                q = intersection_segment_triangle_v3_2(U[i], t)
                                                if q:
                                                    r = q.length()
                                                    O.append((q, r))
                                        else:
                                            print('Fehler 6')

                        else:
                            print('Fehler 4')
        else:
            print('Fehler')
        if len(O) == False: ### no intersection, work on it later
            O.append((vec3(0,0,0), 0))
        else:
            O.sort(key=takesecond, reverse=True) # type: ignore
        X.append(O[0][0])
        R.append(O[0][1])
    return X, R


