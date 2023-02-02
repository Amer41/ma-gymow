from src.psb_modules.retrieve import PSBSet, ModelInfo
from src.psb_modules.classification import ModelClass

from dataclasses import dataclass
import os
import math

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
