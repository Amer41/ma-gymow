from src.psb_modules.retrieve import PSBSet
from src.modules.parsing import read_off
from src.modules.object2 import object2
import math

from dataclasses import dataclass
import os



@dataclass
class FVCalculator():
    psb_set: PSBSet
    number_of_points: int
    winding_speed: int
    p_min: int
    c_number: int
    filename_index: int

    @property
    def fv_file_name(self) -> str:
        return f'FV_{self.number_of_points}_{self.winding_speed}_{self.p_min}_{self.c_number}_{self.filename_index}.txt'


    def compute_FV_PSB(self): # erstellt den Merkmalsvektor für alle Modelle im Benchmark
                                # Merkmalsvektor wird immer in der gleichen Order gespeichert wie das OFF-File des Modells
        directory = self.psb_set.bm_set_path
        confirm = input('do you want to compute all FVs in ' + str(directory) + '? (y/n)')
        if confirm != 'y':
            return
        for dirpath, _, filenames in os.walk(directory):
            if not len(filenames):
                continue
            if self.fv_file_name in filenames:
                continue
            for i in filenames:
                _, ext = os.path.splitext(i)
                if ext != '.off':
                    continue
                file_path_off = os.path.join(dirpath, i)
                vertices, faces = read_off(file_path_off)
                print(file_path_off)
                obj = object2(vertices, faces, self.number_of_points, self.winding_speed, self.p_min, self.c_number)
                file_path_FV = os.path.join(dirpath, self.fv_file_name)
                # file_path_X = os.path.join(dirpath, 'X.txt') # die Koordinaten der X-Kurve können auch erstellt werden
                with open(file_path_FV, 'w') as f:
                    n = len(obj.fv)
                    f.write(str(n) + '\n')
                    for j in obj.fv:
                        f.write(str(j) + ' ')
                # with open(file_path_X, 'w') as f:
                #     n = len(obj.X)
                #     f.write(str(n) + '\n')
                #     for j in obj.X:
                #         f.write(str(j.x) + ' ' + str(j.y) + ' ' + str(j.z) + '\n')

    def delete_FV_PSB(self): # macht die obere Funktion rückgängig
        directory = self.psb_set.bm_set_path
        confirm = input('do you want to remove all FVs from ' + str(directory) + '? (y/n)')
        # directory = 'PSB/test/'
        # directory = 'PSB/psb_test1/benchmark/db/'
        if confirm != 'y':
            return
        for dirpath, _, filenames in os.walk(directory):
            print(dirpath)
            if not len(filenames):
                continue
            if self.fv_file_name not in filenames:
                continue
            file_path_FV = os.path.join(dirpath, self.fv_file_name)
            os.remove(file_path_FV)

    def get_off_PSB(self, modelID: int): # holt ein bestimmtes Modell als object2
        directory = self.psb_set.bm_set_path
        sub_dir_1 = str(math.floor(modelID / 100))
        sub_dir_2 = 'm' + str(modelID)
        file_path_FV = os.path.join(directory, sub_dir_1, sub_dir_2, sub_dir_2 + '.off')
        # print(file_path_FV)
        if os.path.isfile(file_path_FV):
            obj = object2.from_off(file_path_FV, self.number_of_points, self.winding_speed, self.p_min, self.c_number)
            return obj
        else:
            print('file does not exist')
            print(file_path_FV)
            return False

