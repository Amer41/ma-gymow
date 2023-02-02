from src.algorithm_modules.vector3 import vec3
import ipyvolume as ipv
import numpy as np
#  visualisiert Polygonnetz
# nimmt V (Menge der Eckpunkte) und F (Die Indizes der Eckpunkte, welche die Facetten bilden) als Input
def plot_mesh_v3(V: list[vec3], F: list[tuple[int, int, int]], color: str='yellow'):
    x: list[float] = []
    y: list[float] = []
    z: list[float] = []
    for i in V:
        x.append(i.x)
        y.append(i.y)
        z.append(i.z)
    ipv.plot_trisurf(x,y,z, triangles=F, color=color) # type: ignore
    ipv.xyzlim(-30,30) # type: ignore

# visualisiert 3d-Kurve
def plot_3d_curve_v3(U: list[vec3], color:str='red'):
    x: list[float] = []
    y: list[float] = []
    z: list[float] = []
    for i in U:
        x.append(i.x)
        y.append(i.y)
        z.append(i.z)
    x = np.array(x)    # type: ignore
    y = np.array(y)# type: ignore
    z = np.array(z)# type: ignore
    line = ipv.plot(x, y, z, color=color) # type: ignore
def scatter_3d_curve_v3(U: list[vec3], color:str='red'): 
    x: list[float] = []
    y: list[float] = []
    z: list[float] = []
    for i in U:
        x.append(i.x)
        y.append(i.y)
        z.append(i.z)
    x = np.array(x)    # type: ignore
    y = np.array(y)# type: ignore
    z = np.array(z)# type: ignore
    line = ipv.scatter(x, y, z, color=color) # type: ignore