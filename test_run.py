from utils import *
import time
file_paths = []
curves = []
analysers = psb_analysers_all
for i in range(len(analysers)):
    psb_analyser = analysers[i]
    csv_file_path = f'./data/psb_test/curve_{psb_analyser.fv_file_name.split(".")[0]}_test_{i}.csv'
    # curve = read_recall_precision_curve_to_csv(csv_file_path)
    # print(curve)
    # time.sleep(5)
    # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2')
    # exit(1)
    # curves.append(curve)
    file_paths.append(csv_file_path)

plot_rp_curves(analysers, file_paths=file_paths)



    # calculate_results(psb_analyser, f'test_{i}', neigbors_number_list_test)

# create_deatiled_csv_report(psb_analyser, file_path=f'./data/psb_test/table_{psb_analyser.fv_file_name.split(".")[0]}_{run_index}.csv')














