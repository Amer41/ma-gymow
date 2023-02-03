# %%
import numpy as np
import pandas as pd
from src.psb_modules.retrieve import PSBSet, recall_precision_kk, recall_precision_retrieved_models, retrieve_models
from src.psb_modules.calc import FVCalculator
from src.psb_modules.analyse import PSBAnalyser
from src.algorithm_modules.vector3 import Vector3
from src.algorithm_modules.object2 import object2
import ipyvolume as ipv
import matplotlib.pyplot as plt

# psb_set = PSBSet('./psb_v1/')


o1 = object2.from_obj('Porsche_911_GT2.obj', 2000, 40, 64000, 300)
print()

o1.plot_R()
plt.show
# %%
