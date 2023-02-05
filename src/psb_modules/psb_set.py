import os
from dataclasses import dataclass
from typing import ClassVar

from src.psb_modules.classification import PSDClassification

@dataclass
class PSB:
    path: str 

    relative_classification_path: ClassVar[str] = 'benchmark/classification'
    relative_bm_set_path: ClassVar[str] = 'benchmark/db'


    @property
    def bm_set_path(self) -> str:
        return os.path.join(self.path, PSB.relative_bm_set_path)

    @property
    def classifications_path(self) -> str:
        return os.path.join(self.path, PSB.relative_classification_path)

    @property
    def classifications(self) -> PSDClassification:
        return PSDClassification(self.classifications_path)

    def init_psb_fv_variation(self, number_of_points: int, winding_speed: int, p_min:int, c_number: int, filename_index: int) -> 'PSBFVVariantion':
        return PSBFVVariantion(self.path, number_of_points, winding_speed, p_min, c_number, filename_index)



@dataclass
class PSBFVVariantion(PSB):
    number_of_points: int
    winding_speed: int
    p_min: int
    c_number: int
    filename_index: int

    @property
    def fv_file_name(self) -> str:
        return f'FV_{self.number_of_points}_{self.winding_speed}_{self.p_min}_{self.c_number}_{self.filename_index}.txt'

    @property
    def x_file_name(self) -> str:
        return f'X_{self.number_of_points}_{self.winding_speed}_{self.p_min}_{self.c_number}_{self.filename_index}.txt'


    @property
    def directory(self):
        return self.bm_set_path
