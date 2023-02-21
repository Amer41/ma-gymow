from src.psb_modules.psb_set import PSB, PSBFVVariantion
from src.algorithm_modules.utils.parsing import read_off_file
from src.algorithm_modules.feature_vector_extractor import FeatureVectorExtractor
import math


from typing import Optional
import os





class PSBFVCalculator(PSBFVVariantion):
    def __init__(self, path: str, number_of_points: int, winding_speed: int, p_min: int, c_number: int, filename_index: int, sphere_type: str) -> None:
        super().__init__(path, number_of_points, winding_speed, p_min, c_number, filename_index)
        self.sphere_type = sphere_type

    def compute_all_feature_vectors(self): # erstellt den Merkmalsvektor für alle Modelle im Benchmark
                                # Merkmalsvektor wird immer in der gleichen Order gespeichert wie das OFF-File des Modells
        confirm = input('do you want to compute all FVs in ' + str(self.directory) + '? (y/n)')
        if confirm != 'y':
            return
        for dirpath, _, filenames in os.walk(self.directory):
            if not len(filenames):
                continue
            if self.fv_file_name in filenames:
                continue
            for i in filenames:
                _, ext = os.path.splitext(i)
                if ext != '.off':
                    continue
                file_path_off = os.path.join(dirpath, i)
                vertices, faces = read_off_file(file_path_off)
                print(file_path_off)
                obj = FeatureVectorExtractor(vertices, faces, self.number_of_points, self.winding_speed, self.p_min, self.c_number, self.sphere_type)
                file_path_FV = os.path.join(dirpath, self.fv_file_name)
                file_path_X = os.path.join(dirpath, self.x_file_name)
                if not os.path.isfile(file_path_FV):
                    with open(file_path_FV, 'w') as f:
                        n = len(obj.feature_vector)
                        f.write(str(n) + '\n')
                        for j in obj.feature_vector:
                            f.write(str(j) + ' ')
                if not os.path.isfile(file_path_X):
                    with open(file_path_X, 'w') as f:
                        n = len(obj._3d_curve_X)
                        f.write(str(n) + '\n')
                        for j in obj._3d_curve_X:
                            f.write(str(j.x) + ' ' + str(j.y) + ' ' + str(j.z) + '\n')

    def delete_all_feature_vectors(self): # macht die obere Funktion rückgängig
        confirm = input('do you want to remove all FVs from ' + str(self.directory) + '? (y/n)')
        if confirm != 'y':
            return
        for dirpath, _, filenames in os.walk(self.directory):
            print(dirpath)
            if not len(filenames):
                continue
            if self.fv_file_name not in filenames:
                continue
            file_path_FV = os.path.join(dirpath, self.fv_file_name)
            file_path_X = os.path.join(dirpath, self.x_file_name)
            os.remove(file_path_FV)
            os.remove(file_path_X)

    def get_3d_model_with_id(self, modelID: int) -> Optional[FeatureVectorExtractor]: # holt ein bestimmtes Modell als object2
        sub_dir_1 = str(math.floor(modelID / 100))
        sub_dir_2 = 'm' + str(modelID)
        file_path_FV = os.path.join(self.directory, sub_dir_1, sub_dir_2, sub_dir_2 + '.off')
        if os.path.isfile(file_path_FV):
            obj = FeatureVectorExtractor.from_off(file_path_FV, self.number_of_points, self.winding_speed, self.p_min, self.c_number, self.sphere_type)
            return obj
        else:
            print('file does not exist')
            print(file_path_FV)
            return None

