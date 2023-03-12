# %%
from utils import *
# %%
# for i in range(len(psb_analysers_all)):
#     psb_analyser = psb_analysers_all[i]
#     calculate_results(psb_analyser, f'c_{i}', neigbors_number_list_c)
for j in range(len(psb_analysers_all)):
    file_paths = []
    curves = []
    analysers = [psb_analysers_all[j]]
    for i in range(len(analysers)):
        psb_analyser = psb_analysers_all[j]
        csv_file_path = f'./data/psb_c/curve_{psb_analyser.fv_file_name.split(".")[0]}_c_{j}.csv'
        file_paths.append(csv_file_path)

    plot_rp_curves(analysers, file_paths=file_paths)
# %%
