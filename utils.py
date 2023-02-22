from src.psb_modules.psb_set import PSB
from src.psb_modules.calc import PSBFVCalculator
from src.psb_modules.analyse import PSBAnalyser
from src.algorithm_modules.feature_vector_extractor import FeatureVectorExtractor
from src.algorithm_modules.model_descriptor.aabb import AABB
from src.algorithm_modules.model_descriptor.optimized_curve import generate_sphere_with_equidistibuted_points, compute_spherical_helix
from src.algorithm_modules.utils.plotting import *
from time import time

from src.evaluation_modules.recall_and_precision import compute_average_recall_precision_curve
from src.evaluation_modules.retrieval import plot_recall_precision_curves, write_average_recall_precision_curve_to_csv, create_deatiled_csv_report


psb = PSB('../psb-testing/psb_v1/')



psb_calculator_1 = PSBFVCalculator(psb.path, 15000, 200, 64000, 300, 0, 'sin')
psb_analyser_1 = PSBAnalyser(psb.path, 15000, 200, 64000, 300, 0)

psb_calculator_3 = PSBFVCalculator(psb.path, 15000, 0, 64000, 300, 1, 'equi')
psb_analyser_3 = PSBAnalyser(psb.path, 15000, 0, 64000, 300, 1)

psb_calculator_7 = PSBFVCalculator(psb.path, 15000, 0, 64000, 300, 2, 'equi')
psb_analyser_7 = PSBAnalyser(psb.path, 15000, 0, 64000, 300, 2)

psb_calculator_8 = PSBFVCalculator(psb.path, 15000, 0, 64000, 300, 3, 'equi_eigs')
psb_analyser_8 = PSBAnalyser(psb.path, 15000, 0, 64000, 300, 3)

psb_calculator_2 = PSBFVCalculator(psb.path, 2400, 70, 64000, 300, 0, 'sin')
psb_analyser_2 = PSBAnalyser(psb.path, 2400, 70, 64000, 300, 0)

psb_calculator_4 = PSBFVCalculator(psb.path, 2400, 0, 64000, 300, 1, 'equi')
psb_analyser_4 = PSBAnalyser(psb.path, 2400, 0, 64000, 300, 1)

psb_calculator_5 = PSBFVCalculator(psb.path, 2400, 0, 64000, 300, 2, 'equi')
psb_analyser_5 = PSBAnalyser(psb.path, 2400, 0, 64000, 300, 2)

psb_calculator_6 = PSBFVCalculator(psb.path, 2400, 0, 64000, 300, 3, 'equi_eigs')
psb_analyser_6 = PSBAnalyser(psb.path, 2400, 0, 64000, 300, 3)


psb_analysers: list[PSBAnalyser] = [
    psb_analyser_1, psb_analyser_2, psb_analyser_3, psb_analyser_4, psb_analyser_5, psb_analyser_6, psb_analyser_8
    ]
# psb_analysers: list[PSBAnalyser] = [psb_analyser_4, psb_analyser_5]





# ------------------------------------------------------------------------------------------------

def test_run(psb_calculator: PSBFVCalculator):
    start_time = time()
    psb_calculator.compute_all_feature_vectors()
    end_time = time()
    print(f'Execution time: {end_time - start_time} seconds')

def calculate_results(psb_analyser: PSBAnalyser, run_index:int):
    models_test = psb_analyser.get_all_models_info(psb.classifications.base_test)
    models_train = psb_analyser.get_all_models_info(psb.classifications.base_train)

    recall_precision_curve = compute_average_recall_precision_curve(models_test)

    plot_recall_precision_curves([recall_precision_curve])
    write_average_recall_precision_curve_to_csv(recall_precision_curve, file_path=f'./data/test_{run_index}.csv')

    create_deatiled_csv_report(psb_analyser, file_path=f'./data/table_{run_index}.csv')


#  ---------------------------------------------------------------------------------------------

def plot_rp_curves(psb_analysers: list[PSBAnalyser]):
    recall_precision_curves = []
    labels: list[str] = []
    for psb_analyser in psb_analysers:
        models_test = psb_analyser.get_all_models_info(psb.classifications.base_test)
        models_train = psb_analyser.get_all_models_info(psb.classifications.base_train)

        recall_precision_curve = compute_average_recall_precision_curve(models_test)
        recall_precision_curves.append(recall_precision_curve)
        labels.append(psb_analyser.fv_file_name)
    plot_recall_precision_curves(recall_precision_curves, labels)


# -----------------------------------------------------------------------------------------------


