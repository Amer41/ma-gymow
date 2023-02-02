import os
import math
from src.modules.object2 import object2
from src.modules.parsing import read_off
from typing import Union, Any
from src.modules.feature_vectore import compute_distance_2_v3
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

