# %%

from retrieve import *
from src.modules.vector3 import vec3
import ipyvolume as ipv
import matplotlib.pyplot as plt

# %%
# root_dir_norm = r'C:\Users\AmerM\OneDrive - SBL\2021-22\MA\FT\vsc\objekte\OBJ'
o1 = object2.from_obj('Porsche_911_GT2.obj')
print()
# o1.plot_mesh_V3()
# ipv.xyzlim(-2,2)
# ipv.show()
o1.plot_R()
plt.show

# %%
o1.plot_mesh_V3()
ipv.xyzlim(-2, 2)
ipv.show()
# %%
