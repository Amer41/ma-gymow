import os
from src.psb_modules.classification import PSDClassification


class PSBSet:
    relative_classification_path = 'benchmark/classification'
    relative_bm_set_path = 'benchmark/db'

    def __init__(self, set_path: str) -> None:

        self.set_path: str = set_path
        self.bm_set_path: str = os.path.join(set_path, PSBSet.relative_bm_set_path)

        self.classification_path: str = os.path.join(set_path, PSBSet.relative_classification_path)
        self.classifications: PSDClassification = PSDClassification(self.classification_path)