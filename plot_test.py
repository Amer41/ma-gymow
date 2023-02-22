# %%
from utils import *


def show_object_from_psd_plt(psb_calculator: PSBFVCalculator, model_id):
    obj1 = psb_calculator.get_3d_model_with_id(model_id)

    # u = generate_sphere_with_equidistibuted_points()
    if obj1:
        # plot_3d_curve_plt(obj1._3d_curve_X)
        plot_3d_curve_plt(obj1.spherical_helix, 100)
    plt.show()



def show_object_ipv():
    u = generate_sphere_with_equidistibuted_points(2500)
    # u = compute_spherical_helix(2500, 70)
    ipv.figure()
    scatter_3d(u)
    # plot_3d_curve(u)
    ipv.show()

def show_object(sphere_type: str):
    o1 = FeatureVectorExtractor.from_obj('Porsche_911_GT2.obj', 2500, 40, 64000, 300, sphere_type)
    o1.plot_2d_curve_over_time(o1._2d_curve_R)
    plt.show()
# %%
show_object('sin')
show_object('equi')
show_object('equi_eigs')
# %%
o1 = FeatureVectorExtractor.from_obj('Porsche_911_GT2.obj', 15000, 200, 64000, 300, 'sin')
o2 = FeatureVectorExtractor.from_obj('Porsche_911_GT2.obj', 15000, 0, 64000, 300, 'equi')
o3 = FeatureVectorExtractor.from_obj('Porsche_911_GT2.obj', 15000, 0, 64000, 300, 'equi_eigs')


# %%
ipv.figure()
plot_3d_curve(o1._3d_curve_X, 1)
plot_mesh(o3.normalized_vertices_V3, o2.F)
ipv.xyzlim(-2, 2)
ipv.show()
ipv.figure()
plot_3d_curve(o2._3d_curve_X, 1)
plot_mesh(o3.normalized_vertices_V3, o2.F)
ipv.xyzlim(-2,2)
ipv.show()
ipv.figure()
plot_3d_curve(o3._3d_curve_X, 1)
plot_mesh(o3.normalized_vertices_V3, o2.F)
ipv.xyzlim(-2, 2)
ipv.show()

# %%
u1 = FeatureVectorExtractor.from_obj('Porsche_911_GT2.obj', 2400, 100, 64000, 300, 'sin')
u2 = FeatureVectorExtractor.from_obj('Porsche_911_GT2.obj', 2400, 0, 64000, 300, 'equi')
u3 = FeatureVectorExtractor.from_obj('Porsche_911_GT2.obj', 2400, 0, 64000, 300, 'equi_eigs')
u4 = FeatureVectorExtractor.from_obj('Porsche_911_GT2.obj', 2400, 0, 64000, 300, 'equi_aabb')
# %%

ipv.figure()
plot_3d_curve(u1.spherical_helix, 2)
plot_mesh(u3.normalized_vertices_V3, u2.F)
ipv.xyzlim(-2, 2)
ipv.show()
ipv.figure()
plot_3d_curve(u2.spherical_helix, 2)
plot_mesh(u3.normalized_vertices_V3, u2.F)
ipv.xyzlim(-2, 2)
ipv.show()
ipv.figure()
plot_3d_curve(u3.spherical_helix, 2)
plot_mesh(u3.normalized_vertices_V3, u2.F)
ipv.xyzlim(-2, 2)
ipv.show()
ipv.figure()
plot_3d_curve(u4.spherical_helix, 2)
plot_mesh(u4.normalized_vertices_V3, u2.F)
ipv.xyzlim(-2, 2)
ipv.show()



# %%

ipv.figure()
plot_3d_curve(u1._3d_curve_X, 2)
plot_mesh(u3.normalized_vertices_V3, u2.F)
ipv.xyzlim(-2, 2)
ipv.show()
ipv.figure()
plot_3d_curve(u2._3d_curve_X, 2)
plot_mesh(u3.normalized_vertices_V3, u2.F)
ipv.xyzlim(-2, 2)
ipv.show()
ipv.figure()
plot_3d_curve(u3._3d_curve_X, 2)
plot_mesh(u3.normalized_vertices_V3, u2.F)
ipv.xyzlim(-2, 2)
ipv.show()
ipv.figure()
plot_3d_curve(u4._3d_curve_X, 2)
plot_mesh(u4.normalized_vertices_V3, u2.F)
ipv.xyzlim(-2, 2)
ipv.show()


# %%
bounding_box = AABB()
bounding_box.compute_from_list_of_vector3(u1.normalized_vertices_V3)
print(bounding_box)
# %%
