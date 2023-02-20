# %%
from src.algorithm_modules.model_descriptor.optimized_curve import generate_sphere_with_equidistibuted_points
from src.algorithm_modules.utils.plotting import *


u = generate_sphere_with_equidistibuted_points(15000)
scatter_3d_plt(u)
# plot_3d_curve_plt(u)
plt.show()
# ipv.figure()
# scatter_3d(u)
# plot_3d_curve(u)
# ipv.show()




# %%
