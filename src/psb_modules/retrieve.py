import os
import math
from src.modules.object2 import object2
from src.utils.parsing import read_off
from typing import Union, Any
from src.utils.feature_vectore import compute_distance_2_v3
from src.psb_modules.classification import PSDClassification, ModelClass
import numpy as np
from dataclasses import dataclass



class PSBSet:
    relative_classification_path = 'benchmark/classification'
    relative_bm_set_path = 'benchmark/db'

    def __init__(self, set_path: str) -> None:

        self.set_path: str = set_path
        self.bm_set_path: str = os.path.join(set_path, PSBSet.relative_bm_set_path)

        self.classification_path: str = os.path.join(set_path, PSBSet.relative_classification_path)
        self.classifications: PSDClassification = PSDClassification(self.classification_path)

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





@dataclass
class PSBAnalyser:
    psb_set: PSBSet
    number_of_points: int
    winding_speed: int
    p_min: int
    c_number: int
    filename_index: int

    @property
    def fv_file_name(self) -> str:
        return f'FV_{self.number_of_points}_{self.winding_speed}_{self.p_min}_{self.c_number}_{self.filename_index}.txt'

    @property
    def directory(self):
        return self.psb_set.bm_set_path

    def get_FV_PSB(self, modelID: int): # holt der Merkmalsvektor von einem bestimmten Modell aus dem PSB # 
        directory = self.directory
        sub_dir_1 = str(math.floor(modelID / 100))
        sub_dir_2 = 'm' + str(modelID)
        file_path_FV = os.path.join(directory, sub_dir_1, sub_dir_2, self.fv_file_name)
        # print(file_path_FV)
        if os.path.isfile(file_path_FV):
            with open(file_path_FV, 'r') as f:
                _ = int(f.readline())
                fv: list[float] = [float(j) for j in f.readline().strip().split(' ')] # type:ignore
            return fv # type:  ignore
        else:
            print('file does not exist')
            print(file_path_FV)
            return None



    def get_classModels_FV_PSB(self, model_class: ModelClass): # holt modelle die einer bestimmten Klasse angehoren #
                                                    # Die Indizes werden aus dem CLA-File extrahiert
        fvs = []
        for model_node in model_class.models_in_class:
            fv = self.get_FV_PSB(model_node.model_id)
            fvs.append(fv)
        return fvs, model_class.name, model_class.parent_class_name  , model_class.number_of_models 



    def get_modelsWithClassName(self, model_classes: list[ModelClass]): # holt die FVs aller Modelle mit der dazu gehörigen Informationen wie Klassename
        models_info: list[ModelInfo] = []
        for model_class in model_classes:
            for model_node in model_class.models_in_class:
                fv = self.get_FV_PSB(model_node.model_id)
                if fv:
                    models_info.append(ModelInfo(model_node.model_id, fv, model_class.name, model_class.parent_class_name, model_class.number_of_models))
        return models_info

    def get_onemodelpeerclass(self, model_classes: list[ModelClass], model_index: int) -> list['ModelInfo']: # die Modelle im Output wurden als Queries verwerdet, um die Excel-Tabelle zu erstellen
        models_info: list[ModelInfo] = []
        for model_class in model_classes:
            if model_class.number_of_models == 0:
                continue
            model_node = model_class.models_in_class[model_index]
            fv = self.get_FV_PSB(model_node.model_id)
            if fv:
                models_info.append(ModelInfo(model_class.models_in_class[model_index].model_id, fv, model_class.name, model_class.parent_class_name, model_class.number_of_models))
            else:
                print('AAAAAAAAAAA')
        return models_info

@dataclass
class ModelInfo:
    id: int
    fv: list[float]
    class_name: str
    parent_class_name: str
    total_number_of_models_in_class: int

def takesecond(elem): # # dient für die Sortierung von Listen (Sortierung nach dem 2. Element ihrer Mitglieder)
    return elem[1] # 

def retrieve_models(query: ModelInfo, models: list[ModelInfo]): # Abtände der Query zu allen Modelle wird berechnet
    distances: list[tuple[ModelInfo, float]] = []
    for model in models:
        d2 = compute_distance_2_v3(query.fv, model.fv)
        distances.append((model, d2))
    distances.sort(key=takesecond)
    return distances

def recall_precision_retrieved_models(distances_list: list[list[tuple[ModelInfo, float]]], queries: list[ModelInfo], k): # wurde für die erstellung der Excel-Tabelle verwendet
    all_results = []
    for i in range(len(queries)):
        q = queries[i]
        distances = distances_list[i]
        # print(distance)
        rk = 0
        results = []
        results.append(q.parent_class_name + ' - ' + q.class_name + ' - ' + str(q.id))
        for j in range(1, k+1):
            
            results.append(distances[j][0].parent_class_name + ' - ' + distances[j][0].class_name + ' - ' + str(distances[j][0].id))
            if q.class_name == distances[j][0].class_name:
                rk += 1
        recall = rk / (q.total_number_of_models_in_class - 1)
        precision = rk / k
        results.append(q.total_number_of_models_in_class-1)
        results.append(rk)
        
        results.append(recall)
        results.append(precision)
        all_results.append(results)
    return np.array(all_results)

def recall_precision_kk(models: list[ModelInfo], kk): # berechnet Mittelwerte der Trefferquoten und Genauigkeitswerte für alle K in kk
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
        n = i.total_number_of_models_in_class
        for jjj in range(len(models)):
            j = models[jjj]
            if np.array_equal(np.array(i.fv), np.array(j.fv)):
                count += 1
                if count >= 2:
                    pass
            else:
                try:
                    d2 = compute_distance_2_v3(i.fv, j.fv)
                    distances.append((jjj, d2))
                except:
                    print(j.id) # will print the modelID of the defect models
                    pass
        distances.sort(key=takesecond)
        for kkk in range(len(kk)):
            k = kk[kkk]
            rk = 0
            k_ = 0
            for dd in range(k):
                try:
                    d = distances[dd]
                    if i.class_name == models[d[0]].class_name:
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

