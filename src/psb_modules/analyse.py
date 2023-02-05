from src.retrieval_moduls.retrieve import ModelInfo
from src.psb_modules.psb_set import PSB, PSBFVVariantion
from src.psb_modules.classification import ModelClass

from dataclasses import dataclass
import os
import math

@dataclass
class PSBAnalyser(PSBFVVariantion):


    def get_feature_vector_from_model(self, modelID: int):
        sub_dir_1 = str(math.floor(modelID / 100))
        sub_dir_2 = 'm' + str(modelID)
        file_path_FV = os.path.join(self.directory, sub_dir_1, sub_dir_2, self.fv_file_name)
        if os.path.isfile(file_path_FV):
            with open(file_path_FV, 'r') as f:
                _ = int(f.readline())
                fv: list[float] = [float(j) for j in f.readline().strip().split(' ')]
            return fv
        else:
            print('file does not exist')
            print(file_path_FV)
            return None



    # def get_models_with_class_name(self, model_class: ModelClass): # holt modelle die einer bestimmten Klasse angehoren
    #     fvs = []
    #     for model_node in model_class.models_in_class:
    #         fv = self.get_feature_vector_from_model(model_node.model_id)
    #         fvs.append(fv)
    #     return fvs, model_class.name, model_class.parent_class_name  , model_class.number_of_models 



    def get_all_models_info(self, model_classes: list[ModelClass]): # holt die FVs aller Modelle mit der dazu gehörigen Informationen wie Klassename
        models_info: list[ModelInfo] = []
        for model_class in model_classes:
            for model_node in model_class.models_in_class:
                fv = self.get_feature_vector_from_model(model_node.model_id)
                if fv:
                    models_info.append(ModelInfo(model_node.model_id, fv, model_class.name, model_class.parent_class_name, model_class.number_of_models))
        return models_info

    def get_one_model_per_class(self, model_classes: list[ModelClass], model_index: int) -> list['ModelInfo']: # die Modelle im Output wurden als Queries verwerdet, um die Excel-Tabelle zu erstellen
        models_info: list[ModelInfo] = []
        for model_class in model_classes:
            if model_class.number_of_models == 0:
                continue
            model_node = model_class.models_in_class[model_index]
            fv = self.get_feature_vector_from_model(model_node.model_id)
            if fv:
                models_info.append(ModelInfo(model_class.models_in_class[model_index].model_id, fv, model_class.name, model_class.parent_class_name, model_class.number_of_models))
            else:
                print(f'no feature vector found for model with id ({model_node.model_id})')
        return models_info
