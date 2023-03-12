from shapenet import *


# create_deatiled_csv_report_sn(classes, sn_analyser_444,nearest_k_neigbors=100, file_path=f'./data/table_{sn_analyser_444.fv_file_name.split(".")[0]}.csv')

# create_deatiled_csv_report_sn(classes, sn_analyser_444, index_query=1, nearest_k_neigbors=100, file_path=f'./data/table_{sn_analyser_444.fv_file_name.split(".")[0]}_1.csv')

# create_deatiled_csv_report_sn(classes, sn_analyser_444, index_query=2, nearest_k_neigbors=100, file_path=f'./data/table_{sn_analyser_444.fv_file_name.split(".")[0]}_2.csv')
for i in range(3, 11):
    create_deatiled_csv_report_sn(classes, sn_analyser_444, index_query=i, nearest_k_neigbors=100, file_path=f'./data/table_{sn_analyser_444.fv_file_name.split(".")[0]}_{i}.csv')
