import os
import pandas as pd
from src.algorithm_modules.model_descriptor.feature_vector import compute_distance
import numpy as np
from dataclasses import dataclass



@dataclass
class ModelInfo:
    id: int
    fv: list[float]
    class_name: str
    parent_class_name: str
    total_number_of_models_in_class: int

def takesecond(elem):
    return elem[1]

def retrieve_models(query: ModelInfo, models: list[ModelInfo]) -> list[tuple[ModelInfo, float]]: # Abtände der Query zu allen Modelle wird berechnet
    distances: list[tuple[ModelInfo, float]] = []
    for model in models:
        d2 = compute_distance(query.fv, model.fv)
        distances.append((model, d2))
    distances.sort(key=takesecond)
    return distances

def retrieve_nearest_k_neigbors(distances_list: list[list[tuple[ModelInfo, float]]], queries: list[ModelInfo], k): # wurde für die erstellung der Excel-Tabelle verwendet
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




def compute_average_recall_precision_curve(models: list[ModelInfo], neignors_number_list: list[int]): # berechnet Mittelwerte der Trefferquoten und Genauigkeitswerte für alle K in kk
                                     # damit lässt sich das Genauigkeit-Trefferquote-Digramm erstellt. 
    
    recall_curves = []
    precision_curves = []
    for _ in range(len(neignors_number_list)):
        recall_curves.append([])
        precision_curves.append([])

    for i in models:
        distances = []
        count = 0
        n = i.total_number_of_models_in_class
        for model_index in range(len(models)):
            model = models[model_index]
            if np.array_equal(np.array(i.fv), np.array(model.fv)):
                count += 1
                if count >= 2:
                    pass
            else:
                d2 = compute_distance(i.fv, model.fv)
                distances.append((model_index, d2))
        distances.sort(key=takesecond)
        for nighbors_number_index in range(len(neignors_number_list)):
            nighbors_number = neignors_number_list[nighbors_number_index]
            rk = 0
            k_ = 0
            for dd in range(nighbors_number):
                try:
                    d = distances[dd]
                    if i.class_name == models[d[0]].class_name:
                        rk += 1
                except:
                    # print(k)
                    # print(len(distances))
                    k_ += 1
            nighbors_number -= k_
            if  nighbors_number != 0:
                recall = rk / (n-1)
                precision = rk / nighbors_number
                recall_curves[nighbors_number_index].append(recall)
                precision_curves[nighbors_number_index].append(precision)
    recall_curves_array = np.array(recall_curves)
    precision_curves_array = np.array(precision_curves)
    return np.array([np.mean(recall_curves_array, axis=1), np.mean(precision_curves_array, axis=1)]).T

