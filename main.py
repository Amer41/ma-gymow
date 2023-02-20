from src.psb_modules.psb_set import PSB
from src.psb_modules.calc import PSBFVCalculator
from src.psb_modules.analyse import PSBAnalyser
from time import time

from src.evaluation_modules.recall_and_precision import compute_average_recall_precision_curve
from src.evaluation_modules.retrieval import plot_recall_precision_curves, write_average_recall_precision_curve_to_csv, create_deatiled_csv_report

psb = PSB('./psb_v1/')


psb_calculator_4 = PSBFVCalculator(psb.path, 2400, 0, 64000, 300, 1)
psb_analyser_4 = PSBAnalyser(psb.path, 2400, 0, 64000, 300, 1)

# psb_calculator_3 = PSBFVCalculator(psb.path, 15000, 0, 64000, 300, 1)
# psb_analyser_3 = PSBAnalyser(psb.path, 15000, 0, 64000, 300, 1)

# psb_calculator_2 = PSBFVCalculator(psb.path, 2400, 70, 64000, 300, 0)
# psb_analyser_2 = PSBAnalyser(psb.path, 2400, 70, 64000, 300, 0)

# psb_calculator = PSBFVCalculator(psb.path, 15000, 50, 64000, 300, 0)
# psb_analyser = PSBAnalyser(psb.path, 15000, 200, 64000, 300, 0)

start_time = time()
psb_calculator_4.compute_all_feature_vectors()
end_time = time()
print(f'Execution time: {end_time - start_time} seconds')

models_test = psb_analyser_4.get_all_models_info(psb.classifications.base_test)
models_train = psb_analyser_4.get_all_models_info(psb.classifications.base_train)

recall_precision_curve = compute_average_recall_precision_curve(models_test)

plot_recall_precision_curves([recall_precision_curve])
write_average_recall_precision_curve_to_csv(recall_precision_curve, file_path='./data/test_4.csv')

create_deatiled_csv_report(psb_analyser_4, file_path='./data/table_4.csv')