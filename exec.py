# %%
import numpy as np
import pandas as pd
from src.psb_modules.retrieve import PSBSet, recall_precision_kk, recall_precision_retrieved_models, retrieve_models
from src.psb_modules.calc import FVCalculator
from src.psb_modules.analyse import PSBAnalyser
from src.algorithm_modules.vector3 import Vector3
import ipyvolume as ipv
import matplotlib.pyplot as plt

psb_set = PSBSet('./psb_v1/')
# %%
# root_dir_norm = r'C:\Users\AmerM\OneDrive - SBL\2021-22\MA\FT\vsc\objekte\OBJ'
# o1 = object2.from_obj('Porsche_911_GT2.obj', 15000, 200, 64000, 300)
# print()
# # o1.plot_mesh_V3()
# # ipv.xyzlim(-2,2)
# # ipv.show()
# o1.plot_R()
# plt.show

# %%

psb_calc = FVCalculator(psb_set, 15000, 200, 64000, 300, 0)
# %%
psb_calc.compute_FV_PSB()
# %%

psb_analyse = PSBAnalyser(psb_set, 15000, 200, 64000, 300, 0)
models_test = psb_analyse.get_modelsWithClassName(psb_analyse.psb_set.classifications.base_test)
models_train = psb_analyse.get_modelsWithClassName(psb_analyse.psb_set.classifications.base_train)

# Genaigkeit-Trefferquote-Werte bei zunehmendes K (in kk)
# kk = [1,2,3,4, 5, 6, 7, 8, 9, 10, 12, 15, 17, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900]
kk = [i for i in range(1,901)]
re_pre1 = recall_precision_kk(models_test, kk)
# re_pre2 = recall_precision_kk(models_train, kk)
arr = np.array([kk, re_pre1.T[0], re_pre1.T[1]]).T
data = pd.DataFrame(arr, columns=['K', 'Trefferquote', 'Genauigkeit'])
print(data)
# %%
data.to_csv('./data/test_1.csv', sep=';')
# %%
# plotten: Genaigkeit-Trefferquote-Digramm
res_pres = [re_pre1]
labels = ['Genaigkeit-Trefferquote-Kurve', 'Label_2']
plt.rcParams['figure.figsize'] = [16, 10]
plt.rcParams.update({'font.size': 40})
plt.xlim(0,100)
plt.ylim(0,100)
plt.xlabel('Trefferquote (%)')
plt.ylabel('Genauigkeit (%)')
plt.grid()
for i in range(len(res_pres)):
    curve_test = res_pres[i] * 100
    plt.plot(curve_test.T[0], curve_test.T[1], label=labels[i], marker='o', linewidth='3')
plt.legend(loc='upper right', prop={'size':40})
plt.show()
# %%


# Erstellt die Excel-Tabellen
psb_analyse = PSBAnalyser(psb_set, 15000, 200, 64000, 300, 0)
mmm = psb_analyse.get_modelsWithClassName(psb_analyse.psb_set.classifications.base_test)
queries = psb_analyse.get_onemodelpeerclass(psb_analyse.psb_set.classifications.base_test, 0)
distances = []
for q in queries:
    dist = retrieve_models(q, models_test)
    distances.append(dist)
table = recall_precision_retrieved_models(distances, queries, 10)
indices = np.array([1,2,3,4,5,6,7,8,9,10, 'Gesuchte Objekte', 'Gefundene Objekte', 'Trefferquote', 'Genauigkeit'])
data = pd.DataFrame(table.T[1:], columns=table.T[0], index=indices)
print(data)
# %%
data.to_csv('./data/table_1.csv', sep=';') # Pfad des Excel-Dokuments



