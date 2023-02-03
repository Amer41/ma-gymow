from src.algorithm_modules.data_structure.vector3 import Vector3

      
def read_obj_file(in_file: str) -> tuple[list[Vector3], list[tuple[int, int, int]]]:
    faces: list[tuple[int, int, int]] = []
    vertices: list[Vector3] = []
    with open(in_file, 'r') as f:
        for line in f:
            if line.startswith('v '):
                _, x, y, z = line.split(' ')
                vertices.append(Vector3(float(x), float(y), float(z)))
            elif line.startswith('f '):
                _, t1, t2, t3 = line.split(' ')
                v1 = int(t1.split('/')[0]) - 1
                v2 = int(t2.split('/')[0]) - 1
                v3 = int(t3.split('/')[0]) - 1
                faces.append((v1, v2, v3))
    if not len(faces) or not len(vertices):
        raise ValueError(f'error, check file: {in_file}')
    else:
         # vertices = V (Menge der Eckpunkte), faces = F (Die Indizes der Eckpunkte, welche die Facetten bilden) 
        return vertices, faces
 


def read_off_file(in_file: str):
    faces: list[tuple[int, int, int]] = []
    vertices: list[Vector3] = []
    with open(in_file, 'r') as f:
        _ = f.readline() # header: OFF
        n_verts, n_faces, n_dontknow = f.readline().strip().split(' ')
        n_verts, n_faces, n_dontknow = int(n_verts), int(n_faces), int(n_dontknow)
        for _ in range(n_verts):
            x, y, z = f.readline().split(' ')
            vertices.append(Vector3(float(x), float(y), float(z)))
        for _ in range(n_faces):
            _, v1, v2, v3 = f.readline().strip().split(' ')   # example: ['3', '13', '12', '11', '\n']
            faces.append((int(v1), int(v2), int(v3))) # muss nicht mit -1 verrechnet werden
    if not len(faces) or not len(vertices):
        raise ValueError(f'error, check file: {in_file}')
    else:
        return vertices, faces