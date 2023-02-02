
from dataclasses import dataclass
import math
import numpy as np

from .matrix3 import Matrix3


@dataclass
class vec3:
    '''
    Eine Klasse für drei-dimensionale Vectoren:
    Diese Klasse wurde selbstständig erstellt, ...
    ... um die rechengeschwindigkeit zu optimieren.
    vec3 = [
        x
        y
        z
    ]
    '''
    x: float
    y: float
    z: float

    def dot(self, other: 'vec3') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def sub(self, other: 'vec3') -> 'vec3':
        return vec3(self.x - other.x,
                    self.y - other.y,
                    self.z - other.z)

    def __sub__(self, other: 'vec3'):
        return self.sub(other)

    def add(self, other: 'vec3') -> 'vec3':
        return vec3(self.x + other.x,
                    self.y + other.y,
                    self.z + other.z)

    def __add__(self, other: 'vec3'):
        return self.add(other)

    def add_to_self(self, other: 'vec3'):
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def multiply_by_scalar(self, scalar: float) -> 'vec3':
        return vec3(self.x * scalar,
                    self.y * scalar,
                    self.z * scalar)

    def multiply_by_vec3(self, other: 'vec3') -> 'vec3':
        return vec3(self.x * other.x,
                    self.y * other.y,
                    self.z * other.z)

    def rith_multiply_by_matrix3(self, matrix3: 'Matrix3'):
        return vec3(matrix3.x_0 * self.x + matrix3.y_0 * self.y + matrix3.z_0 * self.z,
                    matrix3.x_1 * self.x + matrix3.y_1 * self.y + matrix3.z_1 * self.z,
                    matrix3.x_2 * self.x + matrix3.y_2 * self.y + matrix3.z_2 * self.z)

    

    def cross(self, other: 'vec3') -> 'vec3':
        return vec3(self.y * other.z - self.z * other.y,
                    self.z * other.x - self.x * other.z,
                    self.x * other.y - self.y * other.x)

    def length(self) -> float:
        return math.sqrt(self.x * self.x +
                         self.y * self.y +
                         self.z * self.z)

    def __str__(self) -> str:
        return str((self.x, self.y, self.z))

    @staticmethod
    def covariance_matrix(vector_1: 'vec3', vector_2: 'vec3') -> 'Matrix3':
        xx = vector_1.x * vector_2.x
        xy = vector_1.x * vector_2.y
        xz = vector_1.x * vector_2.z
        yy = vector_1.y * vector_2.y
        yz = vector_1.y * vector_2.z
        zz = vector_1.z * vector_2.z
        return Matrix3(xx, xy, xz,
                       xy, yy, yz,
                       xz, yz, zz)

    def to_array(self: 'vec3') -> np.ndarray:
        return np.array([self.x, self.y, self.z], dtype=np.float64) # type: ignore


    def isequal_array(self, array: np.ndarray) -> bool:
        if (not array[0] == self.x) or (not array[1] == self.y) or (not array[2] == self.z):
            return False
        return True

    def isequal_array_rounded(self, array: np.ndarray, r:int) -> bool:
        rounded_array = np.round(array)
        if (not rounded_array[0] == round(self.x, r)) or (not rounded_array[1] == round(self.y, r)) or (not rounded_array[2] == round(self.z, r)):
            print('False: vec - array; rounded')
            return False
        return True

    def isequal_vec3_vec3(self, other:'vec3') -> bool:
        if not self.x == other.x or not self.y == other.y or not self.z == other.z:
            return False
        return True

    def isequal_vec3_vec3_rounded(self, other: 'vec3', r:int) -> bool:
        if not round(self.x , r) == round(other.x, r) or not round(self.y , r)== round(other.y, r) or not round(self.z , r)== round(other.z, r):
            return False
        return True
        
    @classmethod
    def from_array(cls, array) -> 'vec3':                
        x,y,z = array
        return cls(float(x), float(y), float(z))
        
    @classmethod
    def row_vectors_from_matrix(cls, matrix3: 'Matrix3') -> tuple['vec3', 'vec3', 'vec3']:
        return cls(matrix3.x_0, matrix3.y_0, matrix3.z_0), cls(matrix3.x_1, matrix3.y_1, matrix3.z_1), cls(matrix3.x_2, matrix3.y_2, matrix3.z_2)

