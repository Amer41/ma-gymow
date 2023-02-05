# %%
import numpy as np
import pandas as pd
from src.retrieval_moduls.retrieve import recall_precision_kk, recall_precision_retrieved_models, retrieve_models
from src.psb_modules.calc import FVCalculator
from src.psb_modules.analyse import PSBAnalyser
from src.algorithm_modules.data_structure.vector3 import Vector3
from src.algorithm_modules.feature_vector_extractor import FeatureVectorExtractor
import ipyvolume as ipv
import matplotlib.pyplot as plt

# psb_set = PSBSet('./psb_v1/')


o1 = FeatureVectorExtractor.from_obj('Porsche_911_GT2.obj', 2000, 40, 64000, 300)
print()

o1.plot_2d_curve_over_time(o1._2d_curve_R)
plt.show
# %%
