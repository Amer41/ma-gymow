from typing import Union
from dataclasses import dataclass
import math
import numpy as np

if __name__ == '__main__':
# if TYPE_CHECKING:
    from .matrix3 import Matrix3


@dataclass
class vec3:
    x: Union[float, int]
    y: Union[float, int]
    z: Union[float, int]

    def dot(self, other: 'vec3') -> Union[int, float]:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def transform(self, v1: 'vec3', v2: 'vec3', v3: 'vec3'):
        return vec3(self.dot(v1),
                    self.dot(v2),
                    self.dot(v3))

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

    def sumup(self, other: 'vec3'):
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def multiply_scalar(self, scalar: Union[int, float]) -> 'vec3':
        return vec3(self.x * scalar,
                    self.y * scalar,
                    self.z * scalar)

    def multiply_vec3(self, other: 'vec3') -> 'vec3':
        return vec3(self.x * other.x,
                    self.y * other.y,
                    self.z * other.z)

    

    def cross(self, other: 'vec3') -> 'vec3':
        return vec3(self.y * other.z - self.z * other.y,
                    self.z * other.x - self.x * other.z,
                    self.x * other.y - self.y * other.x)

    def length(self) -> float:
        return math.sqrt(self.x * self.x +
                         self.y * self.y +
                         self.z * self.z)

    def covariance_matrix(self, other: 'vec3') -> 'Matrix3':
        xx = self.x * other.x
        xy = self.x * other.y
        xz = self.x * other.z
        yy = self.y * other.y
        yz = self.y * other.z
        zz = self.z * other.z
        return Matrix3(xx, xy, xz,
                       xy, yy, yz,
                       xz, yz, zz)

    def to_array(self: 'vec3') -> np.ndarray[int, np.dtype[np.float64]]:
        return np.array([self.x, self.y, self.z], dtype=np.float64) # type: ignore

    def __str__(self):
        return str((self.x, self.y, self.z))
        


    def isequal_array(self, array: np.ndarray[int, np.dtype[np.float64]]) -> bool:
        if (not array[0] == self.x) or (not array[1] == self.y) or (not array[2] == self.z):
            print('False: vec - array')
            return False
        return True
    def isequal_array_rounded(self, array:np.ndarray[int, np.dtype[np.float64]], r:int) -> bool:
        array = np.round(array, r) # type: ignore
        if (not array[0] == round(self.x, r)) or (not array[1] == round(self.y, r)) or (not array[2] == round(self.z, r)):
            print('False: vec - array; rounded')
            return False
        return True

    def isequal_vec3_vec3(self, other:'vec3') -> bool:
        if not self.x == other.x or not self.y == other.y or not self.z == other.z:
            print('False: vec - vec')
            return False
        return True

    def isequal_vec3_vec3_rounded(self, other: 'vec3', r:int) -> bool:
        if not round(self.x , r) == round(other.x, r) or not round(self.y , r)== round(other.y, r) or not round(self.z , r)== round(other.z, r):
            print('False: vec - vec; rounded')
            return False
        return True
        
    @classmethod
    def from_array(cls, array: np.ndarray[int, np.dtype[np.float64]]) -> 'vec3':
                               
        x,y,z = array
        return cls(float(x), float(y), float(z))
        
    @classmethod
    def from_matrix(cls, matrix3: 'Matrix3') -> tuple['vec3', 'vec3', 'vec3']:
        return cls(matrix3.x_0, matrix3.y_0, matrix3.z_0), cls(matrix3.x_1, matrix3.y_1, matrix3.z_1), cls(matrix3.x_2, matrix3.y_2, matrix3.z_2)

