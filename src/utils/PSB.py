from src.modules.vector3 import vec3
from typing import Union

# from 

def read_off(in_file: str): # liest OFF-Dokumente, nur für Dreiecke
    faces: list[tuple[int, int, int]] = []
    vertices: list[vec3] = []
    with open(in_file, 'r') as f:
        _ = f.readline() # header: OFF
        n_verts, n_faces, n_dontknow = f.readline().strip().split(' ')
        n_verts, n_faces, n_dontknow = int(n_verts), int(n_faces), int(n_dontknow)
        for _ in range(n_verts):
            x, y, z = f.readline().split(' ')
            vertices.append(vec3(float(x), float(y), float(z)))
        for _ in range(n_faces):
            _, v1, v2, v3 = f.readline().strip().split(' ')   # ['3', '13', '12', '11', '\n']
            faces.append((int(v1), int(v2), int(v3))) # muss nicht mit -1 verrechnet werden
    if not len(faces) or not len(vertices):
        raise ValueError(f'error, check file: {in_file}')
    else:
        return vertices, faces

def read_cla(in_file: str): # Liest CLA-Files
    with open(in_file, 'r') as f:
        classification = []
        # benchmark_name, version_num = f.readline().split(' ')
        num_classes, num_models = f.readline().split(' ')
        num_classes, num_models = len(num_classes), len(num_models)
        for line in f:
            if not line.strip(): # leere Zeile
                continue
            elif len(line.strip().split(' ')) == 3:
                class_name, parentClass_name, num_modelsInClass = line.strip().split(' ')
                num_modelsInClass = int(num_modelsInClass)
                models = [parentClass_name, class_name, num_modelsInClass]
            else:
                models.append(int(line)) # type: ignore
                num_modelsInClass -= 1 # type:ignore
                if num_modelsInClass == 0: # type: ignore
                    classification.append(models) # type: ignore
    return classification # type: ignore  # output = [[parentClass_name, class_name, num_modelsInClass, ....models....], [....],[....]....]


