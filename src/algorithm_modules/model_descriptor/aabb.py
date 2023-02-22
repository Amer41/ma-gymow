from dataclasses import dataclass
from src.algorithm_modules.data_structure.blank import Blank
from src.algorithm_modules.data_structure.vector3 import Vector3



class AABB:
    def __init__(self) -> None:
        self.x_range = Range(Blank(), Blank())
        self.y_range = Range(Blank(), Blank())
        self.z_range = Range(Blank(), Blank())


    
    def __initiate_bounding_box_vector3(self, vertex: Vector3):
        self.x_range.set_min(vertex.x)
        self.x_range.set_max(vertex.x)
        self.y_range.set_min(vertex.y)
        self.y_range.set_max(vertex.y)
        self.z_range.set_min(vertex.z)
        self.z_range.set_max(vertex.z)


    def compute_from_list_of_vector3(self, vertices: list[Vector3]):
        self.__initiate_bounding_box_vector3(vertices[0])
        for vertex in vertices:
            self.x_range.adjust_range(vertex.x)
            self.y_range.adjust_range(vertex.y)
            self.z_range.adjust_range(vertex.z)
        if self.bounding_box_isvalid:
            return
        raise BaseException('ERROR: bounding box is not valid') # model is already normalised
        

    def bounding_box_isvalid(self) -> bool:
        if (not self.x_range.min >= 0) or (not self.x_range.max <= 0):
            return False
        if (not self.y_range.min >= 0) or (not self.y_range.max <= 0):
            return False 
        if (not self.z_range.min >= 0) or (not self.z_range.max <= 0):
            return False
        return True

    def __str__(self) -> str:
        return f"x: {str(self.x_range)}\ny: {str(self.y_range)}\nz: {str(self.z_range)}\n"







@dataclass
class Range:
    min: float
    max: float

    def set_min(self, value_to_assign):
        self.min = value_to_assign

    def set_max(self, value_to_assign):
        self.max = value_to_assign

    def adjust_range(self, value_to_be_compared_to:float):
        if self.min > value_to_be_compared_to:
            self.set_min(value_to_be_compared_to)
        if self.max < value_to_be_compared_to:
            self.set_max(value_to_be_compared_to)
        # else:
        #     raise BaseException('an unexpected errer occured while adjusting the range')

    def __str__(self) -> str:
        return f'[{self.min} --> {self.max}]'


