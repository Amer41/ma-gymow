from src.psb_modules.psb_set import PSB
from src.psb_modules.calc import PSBFVCalculator
from src.psb_modules.analyse import PSBAnalyser
from src.psb_modules.classification import PSBModelClass, PSBModelNode
from src.algorithm_modules.feature_vector_extractor import FeatureVectorExtractor
from src.algorithm_modules.model_descriptor.aabb import AABB
from src.algorithm_modules.model_descriptor.optimized_curve import generate_sphere_with_equidistibuted_points, compute_spherical_helix
from src.algorithm_modules.utils.plotting import *
from typing import Optional
from time import time
import json
from dataclasses import dataclass, field
from src.evaluation_modules.recall_and_precision import compute_average_recall_precision_curve, ModelInfo
from src.evaluation_modules.retrieval import plot_recall_precision_curves, write_average_recall_precision_curve_to_csv, create_deatiled_csv_report
import os
import math

psb = PSB('../psb-testing/psb_v1/')
PSB.relative_bm_set_path = ''
print(psb.relative_bm_set_path)

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
                    models_info.append(ModelInfo(model_node.model_id, fv, model_class.name, model_class.parent_class_name, model_class.number_of_models))
        return models_info

    def get_one_model_per_class(self, model_classes: list['SNModelClass'], model_index: int) -> list['ModelInfo']: # die Modelle im Output wurden als Queries verwerdet, um die Excel-Tabelle zu erstellen
        models_info: list[ModelInfo] = []
        for model_class in model_classes:
            if model_class.number_of_models == 0:
                continue
            model_node = model_class.models_in_class[model_index]
            fv = self.get_feature_vector_from_model(model_node.model_id, model_class.id)
            if fv:
                models_info.append(ModelInfo(model_class.models_in_class[model_index].model_id, fv, model_class.name, model_class.parent_class_name, model_class.number_of_models))
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
    for _class in json_file:
        model_class = SNModelClass(_class['name'], _class['synsetId'], _class['numInstances'], str(0))
        class_path = os.path.join(SN_root_path, model_class.id)
        if not os.path.exists(class_path):
            print(class_path)
            continue
        counter += model_class.number_of_models
        models = os.listdir(class_path)
        for model in models:
            model_class.models_in_class.append(SNModelNode(model, model_class))
        classes.append(model_class)
    print(counter)
    return classes

# classification(psb.bm_set_path ,'taxonomy.json')



