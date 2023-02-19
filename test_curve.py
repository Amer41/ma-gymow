
from src.algorithm_modules.model_descriptor.optimized_curve import generate_sphere_with_equidistibuted_points
from src.algorithm_modules.utils.plotting import *


u = generate_sphere_with_equidistibuted_points(5000)
# plt_scatter_3d_curve(u)
# plt.show()
ipv.figure()
scatter_3d(u)
plot_3d_curve(u)
ipv.show()



