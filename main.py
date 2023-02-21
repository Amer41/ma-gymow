
from src.psb_modules.psb_set import PSB
from src.psb_modules.calc import PSBFVCalculator
from src.psb_modules.analyse import PSBAnalyser
from src.algorithm_modules.feature_vector_extractor import FeatureVectorExtractor
from src.algorithm_modules.model_descriptor.optimized_curve import generate_sphere_with_equidistibuted_points
from src.algorithm_modules.utils.plotting import *
from time import time

from src.evaluation_modules.recall_and_precision import compute_average_recall_precision_curve
from src.evaluation_modules.retrieval import plot_recall_precision_curves, write_average_recall_precision_curve_to_csv, create_deatiled_csv_report



def plot_sets(psb_analysers: list[PSBAnalyser]):
    recall_precision_curves = []
    labels: list[str] = []
    for psb_analyser in psb_analysers:
        models_test = psb_analyser.get_all_models_info(psb.classifications.base_test)
        models_train = psb_analyser.get_all_models_info(psb.classifications.base_train)

        recall_precision_curve = compute_average_recall_precision_curve(models_test)
        recall_precision_curves.append(recall_precision_curve)
        labels.append(psb_analyser.fv_file_name)
    plot_recall_precision_curves(recall_precision_curves, labels)
    
def show_object_from_psd(psb_calculator: PSBFVCalculator, model_id):
    obj1 = psb_calculator.get_3d_model_with_id(model_id)

    # u = generate_sphere_with_equidistibuted_points()
    if obj1:
        plot_3d_curve_plt(obj1._3d_curve_X)
    plt.show()


psb = PSB('./psb_v1/')


# psb_calculator_4 = PSBFVCalculator(psb.path, 2400, 0, 64000, 300, 1)
# psb_analyser_4 = PSBAnalyser(psb.path, 2400, 0, 64000, 300, 1)

psb_calculator_1 = PSBFVCalculator(psb.path, 15000, 50, 64000, 300, 0, 'sin')
psb_analyser_1 = PSBAnalyser(psb.path, 15000, 200, 64000, 300, 0)

psb_calculator_2 = PSBFVCalculator(psb.path, 2400, 70, 64000, 300, 0, 'sin')
psb_analyser_2 = PSBAnalyser(psb.path, 2400, 70, 64000, 300, 0)

psb_calculator_3 = PSBFVCalculator(psb.path, 15000, 0, 64000, 300, 1, 'equi')
psb_analyser_3 = PSBAnalyser(psb.path, 15000, 0, 64000, 300, 1)

psb_calculator_4 = PSBFVCalculator(psb.path, 2400, 0, 64000, 300, 1, 'equi')
psb_analyser_4 = PSBAnalyser(psb.path, 2400, 0, 64000, 300, 1)

psb_analysers: list[PSBAnalyser] = [psb_analyser_1, psb_analyser_2, psb_analyser_3, psb_analyser_4]






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


def show_object():
    o1 = FeatureVectorExtractor.from_obj('Porsche_911_GT2.obj', 2000, 40, 64000, 300, 'sin')
    o1.plot_2d_curve_over_time(o1._2d_curve_R)
    plt.show()

# plot_sets(psb_analysers)

# # psb_calculator = PSBFVCalculator()
# u = generate_sphere_with_equidistibuted_points(15000)
# # scatter_3d_plt(u)
# # plot_3d_curve_plt(u)
# scatter_3d_plt(u)
# plt.show()
# # ipv.figure()
# # scatter_3d(u)
# # plot_3d_curve(u)
# # ipv.show()

show_object_from_psd(psb_calculator_2, 100)
show_object_from_psd(psb_calculator_4, 100)