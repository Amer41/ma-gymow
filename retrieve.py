import os
import math
from src.modules.object2 import object2
from src.utils.parsing import read_off
from typing import Union
from src.utils.feature_vectore import compute_distance_2_v3
import numpy as np
from dataclasses import dataclass

class PSDClassifications:
    def __init__(self, classification_path: str) -> None:

        self.base_test = os.path.join(classification_path, 'base/test.cla')
        self.base_train = os.path.join(classification_path, 'base/train.cla')

        self.coarse1_test = os.path.join(classification_path, 'coarse1/coarse1Test.cla')
        self.coarse1_train = os.path.join(classification_path, 'coarse1/coarse1Train.cla')

        self.coarse2_test = os.path.join(classification_path, 'coarse2/coarse2Test.cla')
        self.coarse2_train = os.path.join(classification_path, 'coarse2/coarse2Train.cla')

        self.coarse3_test = os.path.join(classification_path, 'coarse3/coarse3Test.cla')
        self.coarse3_train = os.path.join(classification_path, 'coarse3/coarse3Train.cla')

    @staticmethod
    def read_cla(in_file: str): # Liest CLA-Files
        with open(in_file, 'r') as f:
            classification = []
            # benchmark_name, version_num = f.readline().split(' ')
            num_classes, num_models = f.readline().split(' ')
            num_classes, num_models = len(num_classes), len(num_models)
            for line in f:
                if not line.strip(): # leere Zeile
                    continue
                elif len(line.strip().split(' ')) == 3:
                    class_name, parentClass_name, num_modelsInClass = line.strip().split(' ')
                    num_modelsInClass = int(num_modelsInClass)
                    models = [parentClass_name, class_name, num_modelsInClass]
                else:
                    models.append(int(line)) # type: ignore
                    num_modelsInClass -= 1 # type:ignore
                    if num_modelsInClass == 0: # type: ignore
                        classification.append(models) # type: ignore
        return classification # type: ignore  # output = [[parentClass_name, class_name, num_modelsInClass, ....models....], [....],[....]....]


class PSBSet:
    relative_classification_path = 'benchmark/classification'
    relative_bm_set_path = 'benchmark/db'

    def __init__(self, set_path: str) -> None:

        self.set_path: str = set_path
        self.bm_set_path: str = os.path.join(set_path, PSBSet.relative_bm_set_path)

        self.classification_path: str = os.path.join(set_path, PSBSet.relative_classification_path)
        self.classifications: PSDClassifications = PSDClassifications(self.classification_path)

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





def get_FV_PSB(directory: str, modelID: int): # holt der Merkmalsvektor von einem bestimmten Modell aus dem PSB # type: ignore
    sub_dir_1 = str(math.floor(modelID / 100))
    sub_dir_2 = 'm' + str(modelID)
    file_path_FV = os.path.join(directory, sub_dir_1, sub_dir_2, 'FV.txt')
    # print(file_path_FV)
    if os.path.isfile(file_path_FV):
        with open(file_path_FV, 'r') as f:
            _ = int(f.readline())
            fv = np.array([float(j) for j in f.readline().strip().split(' ')]) # type:ignore
        return fv # type:  ignore
    else:
        print('file does not exist')
        print(file_path_FV)
        return False


def get_classModels_FV_PSB(directory: str, indices): # holt modelle die einer bestimmten Klasse angehoren #type: ignore
                                                # Die Indizes werden aus dem CLA-File extrahiert
    fvs = []
    parentClass_name = indices[0]
    class_name = indices[1]
    num_modelsInClass = indices[2]
    for i in range(num_modelsInClass):
        modelID = indices[i + 3]
        fv = get_FV_PSB(directory, modelID) # type: ignore
        fvs.append(fv) # type: ignore
    return fvs, class_name, parentClass_name  , num_modelsInClass # type: ignore



################################################3

def get_modelsWithClassName(directory: str, indices): # holt die FVs aller Modelle mit der dazu gehörigen Informationen wie Klassename
    models = []
    for i in indices:
        parentClass_name = i[0]
        class_name = i[1]
        num_modelsInClass = i[2]
        for j in range(num_modelsInClass):
            modelID = i[j + 3]
            fv = get_FV_PSB(directory, modelID)
            models.append((np.array(fv), class_name, num_modelsInClass, modelID, parentClass_name))
    return models

def get_onemodelpeerclass(directory, indices, k): # die Modelle im Output wurden als Queries verwerdet, um die Excel-Tabelle zu erstellen
    models = []
    for i in indices:
        parentClass_name = i[0]
        class_name = i[1]
        num_modelsInClass = i[2]
        modelID = i[k + 3]
        fv = get_FV_PSB(directory, modelID)
        models.append((np.array(fv), class_name, num_modelsInClass, modelID, parentClass_name))
    return models


def takesecond(elem): #type: ignore # dient für die Sortierung von Listen (Sortierung nach dem 2. Element ihrer Mitglieder)
    return elem[1] # type: ignore

def retrieve_models(query, models): # Abtände der Query zu allen Modelle wird berechnet
    distances = []
    for i in models:
        d2 = compute_distance_2_v3(query[0], i[0])
        distances.append((i, d2))
    distances.sort(key=takesecond)
    return distances

def recall_precision_retrieved_models(distances, queries, k): # wurde für die erstellung der Excel-Tabelle verwendet
    all_results = []
    for i in range(len(queries)):
        q = queries[i]
        distance = distances[i]
        # print(distance)
        rk = 0
        results = []
        results.append(q[4] + ' - ' + q[1] + ' - ' + str(q[3]))
        for j in range(1, k+1):
            
            results.append(distance[j][0][4] + ' - ' + distance[j][0][1] + ' - ' + str(distance[j][0][3]))
            if q[1] == distance[j][0][1]:
                rk += 1
        recall = rk / (q[2] - 1)
        precision = rk / k
        results.append(q[2]-1)
        results.append(rk)
        
        results.append(recall)
        results.append(precision)
        all_results.append(results)
    return np.array(all_results)

def recall_precision_kk(models, kk): # berechnet Mittelwerte der Trefferquoten und Genauigkeitswerte für alle K in kk
                                     # damit lässt sich das Genauigkeit-Trefferquote-Digramm erstellt. 
    # try statments and k_ has been given due to some dysfunctioning models (can not be opened) 
    # the error is not in the code but in PSB
    plot_re_pre = []
    recalls = []
    precisions = []
    for kkkkk in range(len(kk)):
        recalls.append([])
        precisions.append([])
    for i in models:
        distances = []
        count = 0
        n = i[2]
        for jjj in range(len(models)):
            j = models[jjj]
            if np.array_equal(i[0], j[0]):
                count += 1
                if count >= 2:
                    pass
            else:
                try:
                    d2 = compute_distance_2_v3(i[0], j[0])
                    distances.append((jjj, d2))
                except:
                    # print(j[3]) # will print the modelID of the defect models
                    pass
        distances.sort(key=takesecond)
        for kkk in range(len(kk)):
            k = kk[kkk]
            rk = 0
            k_ = 0
            for dd in range(k):
                try:
                    d = distances[dd]
                    if i[1] == models[d[0]][1]:
                        rk += 1
                except:
                    # print(k)
                    # print(len(distances))
                    k_ += 1
            k -= k_
            if  k != 0:
                recall = rk / (n-1)
                precision = rk / k
                recalls[kkk].append(recall)
                precisions[kkk].append(precision)
    rec = np.array(recalls)
    pre = np.array(precisions)
    return np.array([np.mean(rec, axis=1), np.mean(pre, axis=1)]).T

