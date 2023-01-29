import os
import math
from src.modules.object2 import object2
from src.utils.PSB import read_off
from typing import Union
from src.utils.feature_vectore import compute_distance_2_v3
import numpy as np
def compute_FV_PSB(directory: str): # erstellt den Merkmalsvektor für alle Modelle im Benchmark
                               # Merkmalsvektor wird immer in der gleichen Order gespeichert wie das OFF-File des Modells
    confirm = input('do you want to compute all FVs in ' + str(directory) + '? (y/n)')
    if confirm == 'y':
        for dirpath, _, filenames in os.walk(directory):
            if not len(filenames):
                pass
            else:
                if not 'FV.txt' in filenames:
                    for i in filenames:
                        _, ext = os.path.splitext(i)
                        if ext == '.off':
                            file_path_off = os.path.join(dirpath, i)
                            vertices, faces = read_off(file_path_off)
                            print(file_path_off)
                            obj = object2(vertices, faces)
                            file_path_FV = os.path.join(dirpath, 'FV.txt')
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

def delete_FV_PSB(directory: str): # macht die obere Funktion rückgängig
    confirm = input('do you want to remove all FVs from ' + str(directory) + '? (y/n)')
    # directory = 'PSB/test/'
    # directory = 'PSB/psb_test1/benchmark/db/'
    if confirm == 'y':
        for dirpath, _, filenames in os.walk(directory):
            print(dirpath)
            if not len(filenames):
                pass
            else:
                if 'FV.txt' in filenames:
                    file_path_FV = os.path.join(dirpath, 'FV.txt')
                    os.remove(file_path_FV)





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


def get_off_PSB(directory: str, modelID: int): # holt ein bestimmtes Modell als object2
    sub_dir_1 = str(math.floor(modelID / 100))
    sub_dir_2 = 'm' + str(modelID)
    file_path_FV = os.path.join(directory, sub_dir_1, sub_dir_2, sub_dir_2 + '.off')
    # print(file_path_FV)
    if os.path.isfile(file_path_FV):
        obj = object2.from_off(file_path_FV)
        return obj
    else:
        print('file does not exist')
        print(file_path_FV)
        return False

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

