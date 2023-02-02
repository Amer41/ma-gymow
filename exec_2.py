import numpy as np
import pandas as pd
from src.modules.vector3 import vec3
import ipyvolume as ipv
import matplotlib.pyplot as plt

from src.psb_modules.retrieve import PSBSet, recall_precision_kk, recall_precision_retrieved_models, retrieve_models
from src.psb_modules.calc import FVCalculator
from src.psb_modules.analyse import PSBAnalyser

psb_set = PSBSet('./psb_v1/')

# Erstellt die Excel-Tabellen
psb_analyse = PSBAnalyser(psb_set, 15000, 200, 64000, 300, 0)
models_test = psb_analyse.get_modelsWithClassName(psb_analyse.psb_set.classifications.base_test)
mmm = psb_analyse.get_modelsWithClassName(psb_analyse.psb_set.classifications.base_test)
queries = psb_analyse.get_onemodelpeerclass(psb_analyse.psb_set.classifications.base_test, 0)
distances = []
for q in queries:
    dist = retrieve_models(q, models_test)
    distances.append(dist)
table = recall_precision_retrieved_models(distances, queries, 10)
indices = np.array([1,2,3,4,5,6,7,8,9,10, 'Gesuchte Objekte', 'Gefundene Objekte', 'Trefferquote', 'Genauigkeit'])
data = pd.DataFrame(table.T[1:], columns=table.T[0], index=indices)
# print(data)
data.to_csv('./data/table_1.csv', sep=';') # Pfad des Excel-Dokuments
