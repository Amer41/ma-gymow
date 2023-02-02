# Es wird eine Klasse für Dreiecke erstellt.
# Dabei werden die konstanten beim MT-Algorithmus zum Bestimmen
# der Schnittpunkte zwischen einem Strahl und einem Dreieck
# berechnet, welche nicht vom Strahl abhängig sind, und in der Klasse gespeichert.
from src.algorithm_modules.vector3 import vec3

class triangle:
    # origin = vec3(0,0,0)
    def __init__(self, v1: vec3 , v2: vec3, v3: vec3):
        self.b = v2
        self.c = v3
        self.a = v1
        self.ab = self.b.sub(self.a)
        self.ac = self.c.sub(self.a)
        self.normal = self.ac.cross(self.ab)
        self.tvec = self.a.multiply_by_scalar(-1) # nur wenn Ursprung des Vektors im Ursprung ist (origin - a) = a * -1
        self.u_constant = self.ac.cross(self.tvec)
        self.v_constant = self.tvec.cross(self.ab)
        self.t = self.v_constant.dot(self.ac)
        self.x = [v1.x, v2.x, v3.x]
        self.y = [v1.y, v2.y, v3.y]
        self.z = [v1.z, v2.z, v3.z]
        

    def __str__(self):
        return str(str(self.a) + '\n ' +
                    str(self.b) + '\n ' +
                    str(self.c))