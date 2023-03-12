from src.psb_modules.psb_set import PSB
from src.psb_modules.calc import PSBFVCalculator
from src.psb_modules.classification import PSBModelClass
from src.psb_modules.analyse import PSBAnalyser
from src.algorithm_modules.feature_vector_extractor import FeatureVectorExtractor
from src.algorithm_modules.model_descriptor.aabb import AABB
from src.algorithm_modules.model_descriptor.optimized_curve import generate_sphere_with_equidistibuted_points, compute_spherical_helix
from src.algorithm_modules.utils.plotting import *
from typing import Optional
from time import time

from src.evaluation_modules.recall_and_precision import compute_average_recall_precision_curve
from src.evaluation_modules.retrieval import plot_recall_precision_curves, write_average_recall_precision_curve_to_csv, create_deatiled_csv_report, read_recall_precision_curve_to_csv


psb = PSB('../psb-testing/psb_v1/')

neigbors_number_list_test = [i for i in range(1, 10)]
k2 = [i for i in range(10, 50, 5)]
k22 = [i for i in range(50, 100, 10)]
k3 = [i for i in range(100, 901, 100)]

for i in k2:
    neigbors_number_list_test.append(i)
for i in k22:
    neigbors_number_list_test.append(i)
for i in k3:
    neigbors_number_list_test.append(i)

psb_calculator_1 = PSBFVCalculator(psb.path, 15000, 200, 64000, 300, 0, 'sin')
psb_analyser_1 = PSBAnalyser(psb.path, 15000, 200, 64000, 300, 0)

psb_calculator_3 = PSBFVCalculator(psb.path, 15000, 0, 64000, 300, 1, 'equi')
psb_analyser_3 = PSBAnalyser(psb.path, 15000, 0, 64000, 300, 1)

psb_calculator_5 = PSBFVCalculator(psb.path, 15000, 0, 64000, 300, 2, 'equi')
psb_analyser_5 = PSBAnalyser(psb.path, 15000, 0, 64000, 300, 2)

psb_calculator_7 = PSBFVCalculator(psb.path, 15000, 0, 64000, 300, 3, 'equi_eigs')
psb_analyser_7 = PSBAnalyser(psb.path, 15000, 0, 64000, 300, 3)

psb_calculator_9 = PSBFVCalculator(psb.path, 15000, 0, 64000, 300, 4, 'equi_aabb')
psb_analyser_9 = PSBAnalyser(psb.path, 15000, 0, 64000, 300, 4)


psb_calculator_2 = PSBFVCalculator(psb.path, 2400, 70, 64000, 300, 0, 'sin')
psb_analyser_2 = PSBAnalyser(psb.path, 2400, 70, 64000, 300, 0)

psb_calculator_4 = PSBFVCalculator(psb.path, 2400, 0, 64000, 300, 1, 'equi')
psb_analyser_4 = PSBAnalyser(psb.path, 2400, 0, 64000, 300, 1)

psb_calculator_6 = PSBFVCalculator(psb.path, 2400, 0, 64000, 300, 2, 'equi')
psb_analyser_6 = PSBAnalyser(psb.path, 2400, 0, 64000, 300, 2)

psb_calculator_8 = PSBFVCalculator(psb.path, 2400, 0, 64000, 300, 3, 'equi_eigs')
psb_analyser_8 = PSBAnalyser(psb.path, 2400, 0, 64000, 300, 3)

psb_calculator_10 = PSBFVCalculator(psb.path, 2400, 0, 64000, 300, 4, 'equi_aabb')
psb_analyser_10 = PSBAnalyser(psb.path, 2400, 0, 64000, 300, 4)

psb_calculator_11 = PSBFVCalculator(psb.path, 400, 50, 64000, 150, 11, 'sin')
psb_analyser_11 = PSBAnalyser(psb.path, 400, 50, 64000, 150, 11)

psb_calculator_12 = PSBFVCalculator(psb.path, 400, 0, 64000, 150, 12, 'equi_aabb')
psb_analyser_12 = PSBAnalyser(psb.path, 400, 0, 64000, 150, 12)

psb_calculator_13 = PSBFVCalculator(psb.path, 400, 50, 64000, 300, 13, 'sin')
psb_analyser_13 = PSBAnalyser(psb.path, 400, 50, 64000, 300, 13)

psb_calculator_14 = PSBFVCalculator(psb.path, 400, 0, 64000, 300, 14, 'equi_aabb')
psb_analyser_14 = PSBAnalyser(psb.path, 400, 0, 64000, 300, 14)


psb_analysers_all: list[PSBAnalyser] = [
    psb_analyser_1, psb_analyser_2, psb_analyser_3, psb_analyser_4, psb_analyser_5,
    psb_analyser_6, psb_analyser_7, psb_analyser_8, psb_analyser_9, psb_analyser_10,
    psb_analyser_11, psb_analyser_12, psb_analyser_13, psb_analyser_14
    ]
psb_analysers: list[PSBAnalyser] = [psb_analyser_4, psb_analyser_5]

psb_analysers: list[PSBAnalyser] = [psb_analyser_11, psb_analyser_12]#, psb_analyser_13, psb_analyser_14]

psb_analysers: list[PSBAnalyser] = [psb_analyser_2, psb_analyser_6, psb_analyser_8, psb_analyser_10]



# ------------------------------------------------------------------------------------------------

def test_run(psb_calculator: PSBFVCalculator):
    start_time = time()
    psb_calculator.compute_all_feature_vectors()
    end_time = time()
    print(f'Execution time: {end_time - start_time} seconds')

def calculate_results(psb_analyser: PSBAnalyser, run_index:str, neigbors_number_list: list[int]):
    # classes = PSBModelClass.combine(psb.classifications.base_test, psb.classifications.base_train)
    models = psb_analyser.get_all_models_info(psb.classifications.base_test)
    
    recall_precision_curve = compute_average_recall_precision_curve(models, neigbors_number_list)

    # plot_recall_precision_curves([recall_precision_curve], [psb_analyser.fv_file_name.split(".")[0]])
    write_average_recall_precision_curve_to_csv(recall_precision_curve, neigbors_number_list, file_path=f'./data/psb_test/curve_{psb_analyser.fv_file_name.split(".")[0]}_{run_index}.csv')

    # create_deatiled_csv_report(psb_analyser, file_path=f'./data/psb_test/table_{psb_analyser.fv_file_name.split(".")[0]}_{run_index}.csv')


#  ---------------------------------------------------------------------------------------------

def plot_rp_curves(psb_analysers: list[PSBAnalyser], curves_labels: Optional[list[str]] = None, file_paths: Optional[list[str]] = None):
    recall_precision_curves = []
    labels: list[str] = []
    for i in range(len(psb_analysers)):
        psb_analyser = psb_analysers[i]
        if file_paths == None:
            raise ValueError
            # classes = PSBModelClass.combine(psb.classifications.base_test, psb.classifications.base_train)
            models = psb_analyser.get_all_models_info(psb.classifications.base_test)

            recall_precision_curve = compute_average_recall_precision_curve(models)
           
        else:
            file_path = file_paths[i]
            recall_precision_curve = read_recall_precision_curve_to_csv(file_path)
        if curves_labels is None:
            labels.append(psb_analyser.fv_file_name)
        recall_precision_curves.append(recall_precision_curve)
    if curves_labels is not None:
        labels = curves_labels
    plot_recall_precision_curves(recall_precision_curves, labels)


# -----------------------------------------------------------------------------------------------


