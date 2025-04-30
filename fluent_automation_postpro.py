import ansys.fluent.core as pyfluent

from ansys.fluent.visualization import set_config
from ansys.fluent.visualization.matplotlib import Plots
from ansys.fluent.visualization.pyvista import Graphics
from ansys.fluent.visualization.pyvista import pyvista_windows_manager

set_config(blocking=True, set_view_on_display="isometric")

solver_session = pyfluent.launch_fluent(
    precision="double", processor_count=4, mode="solver", show_gui=True)

solver_session.file.read_case_data(file_name = "geometry/Static Mixer.dat.h5")

graphics = Graphics(solver_session)

mesh = graphics.Meshes["Mesh"]

mesh()


mesh.surfaces_list = ["velocity_inlet_1", "velocity_inlet_2", "pressure_outlet", "wall"]
mesh.show_edges = True

mesh()

mesh.surfaces_list = mesh.surfaces()
print("Available surfaces:   ", mesh.surfaces_list)
mesh.show_edges = True
# Now display

mesh.show_edges = False

plane = graphics.Surfaces["xy-plane"]

plane()

plane.definition.type.allowed_values

plane.definition.type = "plane-surface"

plane()

plane.definition.plane_surface.xy_plane.z = 0.0015

#plane.display("window-3")


vel_cont = graphics.Contours["contourvel-"]

vel_cont.field = "velocity-magnitude"
vel_cont.surfaces = ["wall"]

vel_cont()

vel_cont.display("window-1")
vel_cont.export_image("output/velocity_magnitude_contour.png", width=1920, height=1080)
pyvista_windows_manager.close_windows(solver_session.id, ["window-1"])
vector = graphics.Vectors["velocity-vector"]

vector.field = "velocity-magnitude"
vector.surfaces= ["xy-plane"]

vector.display()
vector.export_image("output/velocity_contour.png", width=1920, height=1080)
vector.scale = 0.5
vector.display()

vector.export_image("output/velocity_contour_scaled.png", width=1920, height=1080)
vector.close()
plots_session_1 = Plots(solver_session)

xy_plot = plots_session_1.XYPlots["velocity-plot"]
xy_plot()
xy_plot.surfaces()

solver_session.results()

solver_session.results()
solver_session.results.surfaces.line_surface["line-1"]= {
        "name":"line-1",
        "p0":[0.0, 0.0, 0.0],
        "p1":[0.0, 1.0, 0.0]
    }

xy_plot.y_axis_function = "velocity-magnitude"
# xy_plot.surfaces_list = ["line"]
# xy_plot()
xy_plot.surfaces = ["line-1"]
xy_plot.direction_vector = [0,1,0]

xy_plot()

from ansys.fluent.visualization import GraphicsWindow
from ansys.fluent.visualization import XYPlot
xy_plot2 = XYPlot(
    solver=solver_session,
    surfaces=["line-1"],
    y_axis_function="velocity-magnitude",
)
window = GraphicsWindow()
window.add_graphics(xy_plot2)
window.show()
window.close()



