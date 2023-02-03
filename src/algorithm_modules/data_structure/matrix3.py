import numpy as np
from dataclasses import dataclass



@dataclass
class Matrix3:
    '''
    Eine Klasse für 3x3-Matrizen:
    Diese Klasse wurde selbstständig erstellt, ...
    ... um die rechengeschwindigkeit zu optimieren.
    Matrix3 = [
        x_0, y_0, z_0
        x_1, y_1, z_1
        x_2, y_2, z_2
    ]
    '''
    x_0: float
    y_0: float
    z_0: float
    x_1: float
    y_1: float
    z_1: float
    x_2: float
    y_2: float
    z_2: float
    
    def multiply_by_scalar(self, scalar: float) -> 'Matrix3':
        return Matrix3(self.x_0 * scalar, self.y_0 * scalar, self.z_0 * scalar,
                       self.x_1 * scalar, self.y_1 * scalar, self.z_1 * scalar,
                       self.x_2 * scalar, self.y_2 * scalar, self.z_2 * scalar)

        
    def add_to_self(self, other: 'Matrix3') -> None:
        self.x_0 += other.x_0 
        self.y_0 += other.y_0
        self.z_0 += other.z_0
        self.x_1 += other.x_1 
        self.y_1 += other.y_1
        self.z_1 += other.z_1
        self.x_2 += other.x_2 
        self.y_2 += other.y_2
        self.z_2 += other.z_2

    def add(self, other: 'Matrix3') -> 'Matrix3':
        return Matrix3(self.x_0 + other.x_0, self.y_0 + other.y_0, self.z_0 + other.z_0,
                       self.x_1 + other.x_1, self.y_1 + other.y_1, self.z_1 + other.z_1,
                       self.x_2 + other.x_2, self.y_2 + other.y_2, self.z_2 + other.z_2)

    def __add__(self, other: 'Matrix3'):
        return self.add(other)
    
    def __str__(self) -> str:
        return ('(' + str((self.x_0, self.y_0, self.z_0)) + '\n ' + 
                      str((self.x_1, self.y_1, self.z_1)) + '\n ' + 
                      str((self.x_2, self.y_2, self.z_2)) + ')' )

    def round(self, decimal_place: int) -> 'Matrix3':
        return Matrix3(round(self.x_0, decimal_place), round(self.y_0, decimal_place), round(self.z_0, decimal_place),
                       round(self.x_1, decimal_place), round(self.y_1, decimal_place), round(self.z_1, decimal_place),
                       round(self.x_2, decimal_place), round(self.y_2, decimal_place), round(self.z_2, decimal_place))


    def to_array(self) -> np.ndarray:
        return np.array([[self.x_0, self.y_0 , self.z_0],
                         [self.x_1, self.y_1 , self.z_1],
                         [self.x_2, self.y_2 , self.z_2]], dtype=np.float64) 

    def isequal_array(self, array) -> bool:
        if ((not self.x_0 == array[0][0]) or (not self.y_0 == array[0][1]) or (not self.z_0 == array[0][2]) or
            (not self.x_1 == array[1][0]) or (not self.y_1 == array[1][1]) or (not self.z_1 == array[1][2]) or
            (not self.x_2 == array[2][0]) or (not self.y_2 == array[2][1]) or (not self.z_2 == array[2][2])):
            return False
        return True


    def isequal_array_rounded(self, array: np.ndarray, decimal_place: int):
        rounded_array = np.round(array, decimal_place)
        rounded_matrix = self.round(decimal_place)
        if rounded_matrix.isequal_array(rounded_array):
            return True
        return False

    @classmethod
    def from_array(cls, array: np.ndarray):
        a, b, c = array
        x_0, y_0, z_0 = a 
        x_1, y_1, z_1 = b
        x_2, y_2, z_2 = c
        return cls(float(x_0), float(y_0), float(z_0),
                   float(x_1), float(y_1), float(z_1),
                   float(x_2), float(y_2), float(z_2))


        
