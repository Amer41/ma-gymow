import numpy as np
import pandas as pd
from src.algorithm_modules.data_structure.vector3 import Vector3
import ipyvolume as ipv
import matplotlib.pyplot as plt

from src.retrieval_moduls.retrieve import recall_precision_kk, recall_precision_retrieved_models, retrieve_models
from src.psb_modules.psb_set import PSB
from src.psb_modules.calc import FVCalculator
from src.psb_modules.analyse import PSBAnalyser

psb_set = PSB('./psb_v1/')


# Erstellt die Excel-Tabellen
psb_analyse = PSBAnalyser(psb_set.set_path, 15000, 200, 64000, 300, 0)
models_test = psb_analyse.get_all_models_info(psb_analyse.classifications.base_test)
mmm = psb_analyse.get_all_models_info(psb_analyse.classifications.base_test)
queries = psb_analyse.get_one_model_per_class(psb_analyse.classifications.base_test, 0)
distances = []
for q in queries:
    dist = retrieve_models(q, models_test)
    distances.append(dist)
table = recall_precision_retrieved_models(distances, queries, 10)
indices = np.array([1,2,3,4,5,6,7,8,9,10, 'Gesuchte Objekte', 'Gefundene Objekte', 'Trefferquote', 'Genauigkeit'])
data = pd.DataFrame(table.T[1:], columns=table.T[0], index=indices)
# print(data)
data.to_csv('./data/table_1.csv', sep=';') # Pfad des Excel-Dokuments
