from src.psb_modules.analyse import PSBAnalyser
from src.psb_modules.psb_set import PSB
from src.evaluation_modules.recall_and_precision import calculate_distances, retrieve_nearest_k_neigbors

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np





def write_average_recall_precision_curve_to_csv(recall_precision_curve, neignors_number_list: list[int] = [k for k in range(1,901)] ,file_path: str ='./data/test_1.csv'):
    arr = np.array([neignors_number_list, recall_precision_curve.T[0], recall_precision_curve.T[1]]).T
    data = pd.DataFrame(arr, columns=['K', 'Trefferquote', 'Genauigkeit'])
    # print(data)
    data.to_csv(file_path, sep=';')


def plot_recall_precision_curves(rec_pre_curves, labels: list[str] = ['Genauigkeit-Trefferquote-Kurve'], font_size:float = 40 , legend_size:float = 40 , legend_location:str = 'upper right'):
    # labels = ['Genauigkeit-Trefferquote-Kurve', 'Label_2']
    plt.rcParams['figure.figsize'] = [16, 10]
    plt.rcParams.update({'font.size': font_size})
    plt.xlim(0,100)
    plt.ylim(0,100)
    plt.xlabel('Trefferquote (%)')
    plt.ylabel('Genauigkeit (%)')
    plt.grid()
    for i in range(len(rec_pre_curves)):
        curve_test = rec_pre_curves[i] * 100
        plt.plot(curve_test.T[0], curve_test.T[1], label=labels[i], marker='o', linewidth='3')
    plt.legend(loc=legend_location, prop={'size':legend_size})
    plt.show()



def create_deatiled_csv_report( psb_analyse: PSBAnalyser, index_query: int = 0, nearest_k_neigbors: int = 10, file_path: str= './data/table_1.csv'):
    models_test = psb_analyse.get_all_models_info(psb_analyse.classifications.base_test)
    queries = psb_analyse.get_one_model_per_class(psb_analyse.classifications.base_test, index_query)
    distances = []
    for q in queries:
        dist = calculate_distances(q, models_test)
        distances.append(dist)
    table = retrieve_nearest_k_neigbors(distances, queries, nearest_k_neigbors)
    indices = np.array([1,2,3,4,5,6,7,8,9,10, 'Gesuchte Objekte', 'Gefundene Objekte', 'Trefferquote', 'Genauigkeit'])
    data = pd.DataFrame(table.T[1:], columns=table.T[0], index=indices)
    print(data)
    data.to_csv(file_path, sep=';') # Pfad des Excel-Dokuments

