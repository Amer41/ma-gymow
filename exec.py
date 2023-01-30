# %%

from retrieve import FVCalculator, PSBSet
from src.modules.vector3 import vec3
import ipyvolume as ipv
import matplotlib.pyplot as plt

# %%
# root_dir_norm = r'C:\Users\AmerM\OneDrive - SBL\2021-22\MA\FT\vsc\objekte\OBJ'
# o1 = object2.from_obj('Porsche_911_GT2.obj', 15000, 200, 64000, 300)
# print()
# # o1.plot_mesh_V3()
# # ipv.xyzlim(-2,2)
# # ipv.show()
# o1.plot_R()
# plt.show

# %%
psb_set = PSBSet('./psb_v1/')
psb_calc = FVCalculator(psb_set, 15000, 200, 64000, 300, 0)
# %%
psb_calc.compute_FV_PSB()
# %%
