import math
import numpy as np

if __name__ == '__main__':
    from matrix3 import matrix3

# Es wird eine Klasse für 3-dimensionale Vektoren und ihre Operatioen erstellt
class vec3:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, other): # Skalarprodunkt zweier Vektoren
        return self.x * other.x + self.y * other.y + self.z * other.z

    def transform(self, v1, v2, v3): # Vector-Matrix-Multiplikation, v1, v2, v3 sind die Zeilenvectoren der Matrix
        return vec3(self.dot(v1),
                    self.dot(v2),
                    self.dot(v3))

    def sub(self, other): # Vektorsubtraktion
        return vec3(self.x - other.x,
                    self.y - other.y,
                    self.z - other.z)
    def __sub__(self, other):
        return self.sub(other)

    def add(self, other): # Vektoraddition
        return vec3(self.x + other.x,
                    self.y + other.y,
                    self.z + other.z)
    def __add__(self, other):
        return self.add(other)

    def sumup(self, other): # Vektoren werden aufsummiert (das self wird umgeschreiben)
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def multiply_scalar(self, scalar): # Vektor-Skalar-Multiplikatio
        return vec3(self.x * scalar,
                    self.y * scalar,
                    self.z * scalar)

    def multiply_vec3(self, other): # Vector-Vector-Multiplikation, Resultat ist wieder ein Vektor
        return vec3(self.x * other.x,
                    self.y * other.y,
                    self.z * other.z)

    def cross(self, other): # Kreuzprodukt
        return vec3(self.y * other.z - self.z * other.y,
                    self.z * other.x - self.x * other.z,
                    self.x * other.y - self.y * other.x)

    def length(self): # Betrag des Vektors
        return math.sqrt(self.x * self.x +
                         self.y * self.y +
                         self.z * self.z)

    def covariance_matrix(self, other): # berechnet die Kovarianzmatrix des Vektors v: v * v.T
        xx = self.x * other.x
        xy = self.x * other.y
        xz = self.x * other.z
        yy = self.y * other.y
        yz = self.y * other.z
        zz = self.z * other.z
        return matrix3(xx, xy, xz,
                       xy, yy, yz,
                       xz, yz, zz)

    def to_array(self): # convertiert vec3 in Numpy-Array
        return np.array([self.x, self.y, self.z], dtype=np.float64)

    def __str__(self): # zum printen
        return str((self.x, self.y, self.z))
        


    def isequal_array(self, array): # Prüft, ob array und vec3 gleich sind oder nicht ...
                                    # ... Sie können vor dem Prüfen auf eine beliebige Nachkomma stelle gerundet
        if (not array[0] == self.x) or (not array[1] == self.y) or (not array[2] == self.z):
            print('False: vec - array')
            return False
        return True
    def isequal_array_rounded(self, arr, r):
        array = np.round(arr, r)
        if (not array[0] == round(self.x, r)) or (not array[1] == round(self.y, r)) or (not array[2] == round(self.z, r)):
            print('False: vec - array; rounded')
            return False
        return True

    def isequal_vec3_vec3(self, other): # Prüft, ob vec3 und vec3 gleich sind oder nicht
        if not self.x == other.x or not self.y == other.y or not self.z == other.z:
            print('False: vec - vec')
            return False
        return True
    def isequal_vec3_vec3_rounded(self, other, r):
        if not round(self.x , r) == round(other.x, r) or not round(self.y , r)== round(other.y, r) or not round(self.z , r)== round(other.z, r):
            print('False: vec - vec; rounded')
            return False
        return True
        
    @classmethod
    def from_array(vec3, array):# ertellt vec3-Vector aus einem Numpy-Array
                                # Achte darauf, dass die array vom Typ float64 ist (float32 nicht exakt: 3,3 --> 3.29999126)
        x,y,z = array
        return vec3(float(x), float(y), float(z))
        
    @classmethod
    def from_matrix(vec3, m): # matrix3 wird als drei vec3-Vektoren geschrieben
        return vec3(m.x_0, m.y_0, m.z_0), vec3(m.x_1, m.y_1, m.z_1), vec3(m.x_2, m.y_2, m.z_2)

