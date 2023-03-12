import os
from dataclasses import dataclass, field
from typing import Optional

class PSDClassification:
    def __init__(self, classification_path: str) -> None:

        self.base_test = self.read_cla(os.path.join(classification_path, 'v1/base/test.cla'))
        self.base_train = self.read_cla(os.path.join(classification_path, 'v1/base/train.cla'))

        self.coarse1_test = self.read_cla(os.path.join(classification_path, 'v1/coarse1/coarse1Test.cla'))
        self.coarse1_train = self.read_cla(os.path.join(classification_path, 'v1/coarse1/coarse1Train.cla'))

        self.coarse2_test = self.read_cla(os.path.join(classification_path, 'v1/coarse2/coarse2Test.cla'))
        self.coarse2_train = self.read_cla(os.path.join(classification_path, 'v1/coarse2/coarse2Train.cla'))

        self.coarse3_test = self.read_cla(os.path.join(classification_path, 'v1/coarse3/coarse3Test.cla'))
        self.coarse3_train = self.read_cla(os.path.join(classification_path, 'v1/coarse3/coarse3Train.cla'))

    @staticmethod
    def read_cla(in_file: str): # Liest CLA-Files
        classification: list[PSBModelClass] = []
        with open(in_file, 'r') as f:
            benchmark_name, version_num = f.readline().split(' ')
            num_classes, num_models = f.readline().split(' ')
            num_classes, num_models = len(num_classes), len(num_models)
            for line in f:
                if not line.strip(): # leere Zeile
                    continue
                if len(line.strip().split(' ')) == 3:
                    class_name, parentClass_name, num_modelsInClass = line.strip().split(' ')
                    num_modelsInClass = int(num_modelsInClass)
                    model_class = PSBModelClass(class_name, num_modelsInClass, parentClass_name)
                    classification.append(model_class)
                else:
                    model_node = PSBModelNode(int(line))
                    classification[len(classification) - 1].models_in_class.append(model_node)
        return classification  

@dataclass
class PSBModelNode:
    model_id: int
    model_class: Optional['PSBModelClass'] = None

    def __str__(self):
        return str(self.model_id)


@dataclass
class PSBModelClass:
    name: str
    number_of_models: int
    parent_class_name: str
    models_in_class: list[PSBModelNode] = field(default_factory=list)
    child_classes: list['PSBModelClass'] = field(default_factory=list) # unused

    @staticmethod
    def combine(classification_1 : list['PSBModelClass'], classification_2: list['PSBModelClass']):
        class_names : set[str] = set()
        combined_classes : list[PSBModelClass] = []
        classifications = [classification_1, classification_2]
        for classification in classifications:
            for model_class in classification:
                class_names.add(model_class.name)
        for class_name in class_names:
            new_model_class = PSBModelClass(class_name, 0, '0')
            for classification in classifications:
                for model_class in classification:
                    if model_class.name != class_name:
                        continue
                    new_model_class.number_of_models += model_class.number_of_models
                    new_model_class.parent_class_name = model_class.parent_class_name
                    for model_node in model_class.models_in_class:
                        new_model_class.models_in_class.append(model_node)
            for model_node in new_model_class.models_in_class:
                model_node.model_class = new_model_class
            combined_classes.append(new_model_class)
        return combined_classes








