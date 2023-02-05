from src.psb_modules.psb_set import PSB
from src.psb_modules.calc import PSBFVCalculator
from src.psb_modules.analyse import PSBAnalyser

from src.evaluation_modules.recall_and_precision import compute_average_recall_precision_curve
from src.evaluation_modules.retrieval import plot_recall_precision_curves, write_average_recall_precision_curve_to_csv, create_deatiled_csv_report

psb = PSB('./psb_v1/')

psb_calculator = PSBFVCalculator(psb.path, 3000, 50, 64000, 300, 0)
psb_analyser = PSBAnalyser(psb.path, 15000, 200, 64000, 300, 0)

models_test = psb_analyser.get_all_models_info(psb.classifications.base_test)
models_train = psb_analyser.get_all_models_info(psb.classifications.base_train)

recall_precision_curve = compute_average_recall_precision_curve(models_test)

plot_recall_precision_curves([recall_precision_curve])
write_average_recall_precision_curve_to_csv(recall_precision_curve)

create_deatiled_csv_report(psb_analyser)