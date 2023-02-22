from src.algorithm_modules.data_structure.vector3 import Vector3
import ipyvolume as ipv
import numpy as np
import matplotlib.pyplot as plt
#  visualisiert Polygonnetz
# nimmt V (Menge der Eckpunkte) und F (Die Indizes der Eckpunkte, welche die Facetten bilden) als Input

def plot_mesh(vertices: list[Vector3], faces: list[tuple[int, int, int]], color: str='yellow'):
    x: list[float] = []
    y: list[float] = []
    z: list[float] = []
    for i in vertices:
        x.append(i.x)
        y.append(i.y)
        z.append(i.z)
    ipv.plot_trisurf(x,y,z, triangles=faces, color=color)
    # ipv.xyzlim(-30,30)

# visualisiert 3d-Kurve
def plot_3d_curve(curve: list[Vector3], plot_scale: float = 1, color: str='red'):
    x: list[float] = []
    y: list[float] = []
    z: list[float] = []
    for i in curve:
        x.append(i.x)
        y.append(i.y)
        z.append(i.z)
    x_array = np.array(x) * plot_scale
    y_array = np.array(y) * plot_scale  
    z_array = np.array(z) * plot_scale  
    line = ipv.plot(x_array, y_array, z_array, color=color)


def scatter_3d(point_set: list[Vector3], plot_scale: float = 1, color: str='red'):
    x: list[float] = []
    y: list[float] = []
    z: list[float] = []
    for i in point_set:
        x.append(i.x)
        y.append(i.y)
        z.append(i.z)
    x_array = np.array(x) * plot_scale
    y_array = np.array(y) * plot_scale
    z_array = np.array(z) * plot_scale
    ipv.scatter(x_array, y_array, z_array, color=color, size=5)



def plot_3d_curve_plt(point_set: list[Vector3], plot_scale: float = 1, color: str='red'):
    x: list[float] = []
    y: list[float] = []
    z: list[float] = []
    for i in point_set:
        x.append(i.x)
        y.append(i.y)
        z.append(i.z)
    x_array = np.array(x) * plot_scale
    y_array = np.array(y) * plot_scale
    z_array = np.array(z) * plot_scale
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.axis('equal')
    ax.axis([-2, 2, -2, 2])
    ax.plot(x_array,y_array,z_array, color)

def scatter_3d_plt(point_set: list[Vector3], plot_scale: float = 1, color: str='red'):
    x: list[float] = []
    y: list[float] = []
    z: list[float] = []
    for i in point_set:
        x.append(i.x)
        y.append(i.y)
        z.append(i.z)
    x_array = np.array(x) * plot_scale
    y_array = np.array(y) * plot_scale
    z_array = np.array(z) * plot_scale
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter(x_array,y_array,z_array, linewidths=0.5)
