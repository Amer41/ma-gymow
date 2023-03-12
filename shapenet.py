
from src.psb_modules.psb_set import PSB
from src.psb_modules.calc import PSBFVCalculator
from src.psb_modules.analyse import PSBAnalyser
from src.algorithm_modules.utils.plotting import *
from typing import Optional, Union
from time import time
import json
from dataclasses import dataclass, field
# from src.evaluation_modules.recall_and_precision import compute_average_recall_precision_curve, ModelInfo, calculate_distances
from src.evaluation_modules.retrieval import plot_recall_precision_curves, write_average_recall_precision_curve_to_csv, create_deatiled_csv_report
import os
import pandas as pd
import math


def compute_distance(feature_vector_1: np.ndarray, feature_vector_2: np.ndarray):
    # N = len(feature_vector_1)
    # d2 = 0
    # for i in range(N):
    array = (feature_vector_1 - feature_vector_2)
    array = array*array
    d2 = np.sum(array)
    d2 = math.sqrt(d2)
    return d2

@dataclass
class ModelInfo:
    id: Union[int, str]
    fv: np.ndarray
    class_name: str
    parent_class_name: str
    total_number_of_models_in_class: int

def takesecond(elem):
    return elem[1]

def calculate_distances(query: ModelInfo, models: list[ModelInfo]) -> list[tuple[ModelInfo, float]]: # Abtände der Query zu allen Modelle wird berechnet
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




def compute_average_recall_precision_curve(models: list[ModelInfo], neigbors_number_list: list[int] = [k for k in range(1,901)]): # berechnet Mittelwerte der Trefferquoten und Genauigkeitswerte für alle K in kk
                                     # damit lässt sich das Genauigkeit-Trefferquote-Digramm erstellt. 
    
    recall_curves = []
    precision_curves = []
    for _ in range(len(neigbors_number_list)):
        recall_curves.append([])
        precision_curves.append([])

    for i in models:
        distances = []
        count = 0
        n = i.total_number_of_models_in_class
        for model_index in range(len(models)):
            model = models[model_index]
            if np.array_equal(i.fv, model.fv):
                count += 1
                if count >= 2:
                    pass
            else:
                d2 = compute_distance(i.fv, model.fv)
                distances.append((model_index, d2))
        distances.sort(key=takesecond)
        # Genaigkeit-Trefferquote-Werte bei zunehmendes k
        for nighbors_number_index in range(len(neigbors_number_list)):
            nighbors_number = neigbors_number_list[nighbors_number_index]
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
    recall_precision_curve = np.array([np.mean(recall_curves_array, axis=1), np.mean(precision_curves_array, axis=1)]).T
    return recall_precision_curve



'''
the methods of PSBAnalyser has been modified in order...
... to match the file structure of the ShapeNet dataset.
the output of PSBAnalyser and SNAnalyser is of the ...
... same type, which means the same evaluation methods...
can be used for both.
Note: SNAnalyser does not use the classification class...
of the PSB super class.
'''


class SNAnalyser(PSBAnalyser):
    def get_feature_vector_from_model(self, model_id: str, class_id: str):
        sub_dir_2 = model_id
        sub_dir_1 = class_id
        file_path_FV = os.path.join(self.directory, sub_dir_1, sub_dir_2, 'models', self.fv_file_name)
        if os.path.isfile(file_path_FV):
            with open(file_path_FV, 'r') as f:
                _ = int(f.readline())
                fv: list[float] = [float(j) for j in f.readline().strip().split(' ')]
            return fv
        else:
            print('file does not exist')
            print(file_path_FV)
            return None



    def get_all_models_info(self, model_classes: list['SNModelClass']): # holt die FVs aller Modelle mit der dazu gehörigen Informationen wie Klassename
        models_info: list[ModelInfo] = []
        for model_class in model_classes:
            for model_node in model_class.models_in_class:
                fv = self.get_feature_vector_from_model(model_node.model_id, model_class.id)
                if fv:
                    models_info.append(ModelInfo(model_node.model_id, np.array(fv, dtype=np.float64), model_class.name, model_class.parent_class_name, model_class.number_of_models))
        return models_info

    def get_one_model_per_class(self, model_classes: list['SNModelClass'], model_index: int) -> list['ModelInfo']: # die Modelle im Output wurden als Queries verwerdet, um die Excel-Tabelle zu erstellen
        models_info: list[ModelInfo] = []
        for model_class in model_classes:
            if model_class.number_of_models == 0:
                continue
            model_node = model_class.models_in_class[model_index]
            fv = self.get_feature_vector_from_model(model_node.model_id, model_class.id)
            if fv:
                models_info.append(ModelInfo(model_class.models_in_class[model_index].model_id, np.array(fv, dtype=np.float64), model_class.name, model_class.parent_class_name, model_class.number_of_models))
            else:
                print(f'no feature vector found for model with id ({model_node.model_id})')
        return models_info

@dataclass
class SNModelNode:
    model_id: str
    model_class: Optional['SNModelClass'] = None

    def __str__(self):
        return self.model_id


@dataclass
class SNModelClass:
    name: str
    id: str
    number_of_models: int
    parent_class_name: str
    models_in_class: list[SNModelNode] = field(default_factory=list)
    child_classes: list['SNModelClass'] = field(default_factory=list) # unused

def classification(SN_root_path: str, json_file_path: str) -> list[SNModelClass]:
    classes : list[SNModelClass] = []
    counter = 0
    with open(json_file_path, 'r') as f:
        json_file = json.load(f)
    not_found_models = ['207e69af994efa9330714334794526d4','2307b51ca7e4a03d30714334794526d4','302612708e86efea62d2c237bfbc22ca','3c33f9f8edc558ce77aa0b62eed1492','3ffeec4abd78c945c7c79bdb1d5fe365','407f2811c0fe4e9361c6c61410fc904b','4ddef66f32e1902d3448fdcb67fe08ff','5973afc979049405f63ee8a34069b7c5','5bf2d7c2167755a72a9eb0f146e94477','7aa9619e89baaec6d9b8dfa78596b717','806d740ca8fad5c1473f10e6caaeca56','8070747805908ae62a9eb0f146e94477','93ce8e230939dfc230714334794526d4','986ed07c18a2e5592a9eb0f146e94477','9fb1d03b22ecac5835da01f298003d56','d6ee8e0a0b392f98eb96598da750ef34','e6c22be1a39c9b62fb403c87929e1167','ea3f2971f1c125076c4384c3b17a86ea','f5bac2b133a979c573397a92d1662ba5']
    for _class in json_file:
        model_class = SNModelClass(_class['name'], _class['synsetId'], _class['numInstances'], str(0))
        if model_class.id == '02958343': # has missing modules (not_found_models)
            model_class.number_of_models -= len(not_found_models)
        class_path = os.path.join(SN_root_path, model_class.id)
        if not os.path.exists(class_path):
            # print(class_path)
            continue
        counter += model_class.number_of_models
        models = os.listdir(class_path)
        for model in models:
            if model in not_found_models:
                continue
            model_class.models_in_class.append(SNModelNode(model, model_class))
        classes.append(model_class)
    print(counter)
    return classes




def create_deatiled_csv_report_sn(classes: list[SNModelClass], psb_analyse: SNAnalyser, index_query: int = 0, nearest_k_neigbors: int = 10, file_path: str= './data/table_1.csv'):
    models_test = psb_analyse.get_all_models_info(classes)
    queries = psb_analyse.get_one_model_per_class(classes, index_query)
    distances = []
    for q in queries:
        dist = calculate_distances(q, models_test)
        distances.append(dist)
    table = retrieve_nearest_k_neigbors(distances, queries, nearest_k_neigbors)
    iiii: list[Union[int, str]] = [i for i in range(1, nearest_k_neigbors+1)]
    iiii.append('Gesuchte Objekte')
    iiii.append('Gefundene Objekte')
    iiii.append('Trefferquote')
    iiii.append('Genauigkeit')
    indices = np.array(iiii)
    # indices = np.array([1,2,3,4,5,6,7,8,9,10, 'Gesuchte Objekte', 'Gefundene Objekte', 'Trefferquote', 'Genauigkeit'])
    data = pd.DataFrame(table.T[1:], columns=table.T[0], index=indices)
    print(data)
    
    data.to_csv(file_path, sep=';') # Pfad des Excel-Dokuments
def calculate_results_sn(psb_analyser: SNAnalyser, file_path:str, classes: list[SNModelClass], neigbors_number_list:list[int]):
    models_test = psb_analyser.get_all_models_info(classes)

    recall_precision_curve = compute_average_recall_precision_curve(models_test, neigbors_number_list)

    write_average_recall_precision_curve_to_csv(recall_precision_curve, neigbors_number_list, file_path= file_path)
    plot_recall_precision_curves([recall_precision_curve])

    # create_deatiled_csv_report_sn(classes, psb_analyser, file_path=f'./data/table_{run_index}.csv')


#  ---------------------------------------------------------------------------------------------

def plot_rp_curves_sn(classes: list[SNModelClass], sn_analysers: list[SNAnalyser], curves_labels: Optional[list[str]] = None):
    recall_precision_curves = []
    labels: list[str] = []
    for psb_analyser in sn_analysers:
        models_test = psb_analyser.get_all_models_info(classes)

        recall_precision_curve = compute_average_recall_precision_curve(models_test)
        recall_precision_curves.append(recall_precision_curve)
        if curves_labels is None:
            labels.append(psb_analyser.fv_file_name)
    if curves_labels is not None:
        labels = curves_labels
    plot_recall_precision_curves(recall_precision_curves, labels)


# -----------------------------------------------------------------------------------------------
psb = PSB('../shapenet/models_fv')
PSB.relative_bm_set_path = ''
classes = classification(psb.bm_set_path ,'taxonomy.json')

counter = 0
print(len(classes))
print('the following classes do not have the right numbers of models:')
for class_ in classes:
    counter += class_.number_of_models
    if class_.number_of_models != len(class_.models_in_class):
        print(class_.id)
print(counter)

sn_analyser_222 = SNAnalyser(psb.path, 400, 50, 64000, 150, 222)
sn_analyser_444 = SNAnalyser(psb.path, 400, 50, 64000, 150, 444)