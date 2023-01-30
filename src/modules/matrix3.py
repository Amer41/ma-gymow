import numpy as np
from dataclasses import dataclass
from typing import Union





@dataclass
class Matrix3:
    x_0: Union[float, int]
    y_0: Union[float, int]
    z_0: Union[float, int]
    x_1: Union[float, int]
    y_1: Union[float, int]
    z_1: Union[float, int]
    x_2: Union[float, int]
    y_2: Union[float, int]
    z_2: Union[float, int]
    # def __init__(self, x_0, y_0, z_0,
    #                    x_1, y_1, z_1,
    #                    x_2, y_2, z_2):
    #     self.x_0, self.y_0, self.z_0 = x_0, y_0, z_0
    #     self.x_1, self.y_1, self.z_1 = x_1, y_1, z_1
    #     self.x_2, self.y_2, self.z_2 = x_2, y_2, z_2
    
    def multiply_scalar(self, scalar: Union[int, float]): # matrix-skalar-multiplikation
        return Matrix3(self.x_0 * scalar, self.y_0 * scalar, self.z_0 * scalar,
                       self.x_1 * scalar, self.y_1 * scalar, self.z_1 * scalar,
                       self.x_2 * scalar, self.y_2 * scalar, self.z_2 * scalar)

    # def multiply_vec3(self, v: 'vec3'): # matrix-vector-multiplikation
    #     return vec3(self.x_0 * v.x + self.y_0 * v.y + self.z_0 * v.z,
    #                 self.x_1 * v.x + self.y_1 * v.y + self.z_1 * v.z,
    #                 self.x_2 * v.x + self.y_2 * v.y + self.z_2 * v.z)
        
    def sumup(self, other: 'Matrix3'): # aufsummierung (self wird übergeschrieben)
        self.x_0 += other.x_0 
        self.y_0 += other.y_0
        self.z_0 += other.z_0
        self.x_1 += other.x_1 
        self.y_1 += other.y_1
        self.z_1 += other.z_1
        self.x_2 += other.x_2 
        self.y_2 += other.y_2
        self.z_2 += other.z_2

    def add(self, other: 'Matrix3'): # matrix addition
        return Matrix3(self.x_0 + other.x_0, self.y_0 + other.y_0, self.z_0 + other.z_0,
                       self.x_1 + other.x_1, self.y_1 + other.y_1, self.z_1 + other.z_1,
                       self.x_2 + other.x_2, self.y_2 + other.y_2, self.z_2 + other.z_2)

    def __add__(self, other: 'Matrix3'):
        return self.add(other)
    
    def __str__(self): # zum printen
        return ('(' + str((self.x_0, self.y_0, self.z_0)) + '\n ' + 
                      str((self.x_1, self.y_1, self.z_1)) + '\n ' + 
                      str((self.x_2, self.y_2, self.z_2)) + ')' )

    def to_array(self): # matrix3 in numpy-array
        return np.array([[self.x_0, self.y_0 , self.z_0], # type: ignore
                         [self.x_1, self.y_1 , self.z_1],
                         [self.x_2, self.y_2 , self.z_2]], dtype=np.float64) 

    def isequal_array(self, array): # gleichheitprüfung: matrix3 numpy_array
        if ((not self.x_0 == array[0][0]) or (not self.y_0 == array[0][1]) or (not self.z_0 == array[0][2]) or
            (not self.x_1 == array[1][0]) or (not self.y_1 == array[1][1]) or (not self.z_1 == array[1][2]) or
            (not self.x_2 == array[2][0]) or (not self.y_2 == array[2][1]) or (not self.z_2 == array[2][2])):
            print('False: mat3 - array')
            return False
        return True
    def round(self, r: int):
        return Matrix3(round(self.x_0, r), round(self.y_0, r), round(self.z_0, r),
                       round(self.x_1, r), round(self.y_1, r), round(self.z_1, r),
                       round(self.x_2, r), round(self.y_2, r), round(self.z_2, r))
    def isequal_array_rounded(self, arr, r: int):
        array = np.round(arr, r) #type: ignore
        matrix = self.round(r)
        if ((not matrix.x_0 == array[0][0]) or (not matrix.y_0 == array[0][1]) or (not matrix.z_0 == array[0][2]) or
            (not matrix.x_1 == array[1][0]) or (not matrix.y_1 == array[1][1]) or (not matrix.z_1 == array[1][2]) or
            (not matrix.x_2 == array[2][0]) or (not matrix.y_2 == array[2][1]) or (not matrix.z_2 == array[2][2])):
            print('False: mat3 - array; rounded')
            return False
        return True

    @classmethod
    def from_array(cls, array): # erstellt matrix3 aus numpy_array
        a, b, c = array
        x_0, y_0, z_0 = a 
        x_1, y_1, z_1 = b
        x_2, y_2, z_2 = c
        return cls(float(x_0), float(y_0), float(z_0),
                       float(x_1), float(y_1), float(z_1),
                       float(x_2), float(y_2), float(z_2))


        
