from src.algorithm_modules.data_structure.vector3 import Vector3

class Triangle:
    
    def __init__(self, v1: Vector3 , v2: Vector3, v3: Vector3):
        self.a = v1
        self.b = v2
        self.c = v3

        self.a_minus_b = self.b.sub(self.a)
        self.a_minus_c = self.c.sub(self.a)

        self.normal_vector = self.a_minus_c.cross(self.a_minus_b)
        
        self.t_vector = self.a.multiply_by_scalar(-1) # nur wenn Ursprung des Vektors im Ursprung ist (origin - a) = a * -1

        self.u_constant = self.a_minus_c.cross(self.t_vector)
        self.v_constant = self.t_vector.cross(self.a_minus_b)

        self.t_contsant = self.v_constant.dot(self.a_minus_c)

        self.x_coordinate_of_vertices = [v1.x, v2.x, v3.x]
        self.y_coordinate_of_vertices = [v1.y, v2.y, v3.y]
        self.z_coordinate_of_vertices = [v1.z, v2.z, v3.z]
        

    def __str__(self):
        return str(str(self.a) + '\n ' +
                    str(self.b) + '\n ' +
                    str(self.c))