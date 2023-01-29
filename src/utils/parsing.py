from src.modules.vector3 import vec3


def read_obj_v3(in_file: str) -> tuple[list[vec3], list[tuple[int, int, int]]]: # liest OBJ-Dateiformat, funktioniert nur mit Dreiecken
    faces: list[tuple[int, int, int]] = []
    vertices: list[vec3] = []
    with open(in_file, 'r') as f:
        for line in f:
            if line.startswith('v '):
                _, x, y, z = line.split(' ')
                vertices.append(vec3(float(x), float(y), float(z)))
            elif line.startswith('f '):
                _, t1, t2, t3 = line.split(' ')
                v1 = int(t1.split('/')[0]) - 1
                v2 = int(t2.split('/')[0]) - 1
                v3 = int(t3.split('/')[0]) - 1
                faces.append((v1, v2, v3))
    if not len(faces) or not len(vertices):
        raise ValueError(f'error, check file: {in_file}')
    else:
        return vertices, faces
# vertices = V (Menge der Eckpunkte), faces = F (Die Indizes der Eckpunkte, welche die Facetten bilden)        