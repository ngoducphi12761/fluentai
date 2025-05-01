import os
import yaml
import ansys.fluent.core as pyfluent
import datetime
import shutil
# from ansys.fluent.visualization import set_config
# from ansys.fluent.visualization.matplotlib import Plots
# from ansys.fluent.visualization.pyvista import Graphics


class FluentMeshing:
    """Handles meshing operations in Fluent."""

    def __init__(self):
        self.session, self.workflow = self.initialize_meshing_session()

    @staticmethod
    def initialize_meshing_session():
        """Launch and initialize the meshing session."""
        meshing_session = pyfluent.launch_fluent(
            show_gui=True,
            mode="meshing",
            precision="double",
            processor_count=4,
            additional_arguments="-driver opengl"
        )
        workflow = meshing_session.workflow
        meshing = meshing_session.meshing
        workflow.InitializeWorkflow(WorkflowType=r'Watertight Geometry')
        meshing.GlobalSettings.LengthUnit.set_state(r'mm')
        return meshing_session, workflow

    def import_geometry(self, geometry_path):
        """Import the geometry file into the workflow."""
        self.workflow.TaskObject['Import Geometry'].Arguments.set_state({"FileName": geometry_path})
        self.workflow.TaskObject['Import Geometry'].Execute()

    def setup_meshing(self):
        """Set up meshing tasks."""
        workflow = self.workflow
        workflow.TaskObject['Add Local Sizing'].AddChildAndUpdate()
        workflow.TaskObject['Generate the Surface Mesh'].Execute()
        workflow.TaskObject['Describe Geometry'].Arguments.set_state(
            {r'SetupType': r'The geometry consists of only fluid regions with no voids'}
        )
        workflow.TaskObject['Describe Geometry'].UpdateChildTasks(SetupTypeChanged=True)
        workflow.TaskObject['Describe Geometry'].Execute()
        workflow.TaskObject['Update Boundaries'].Execute()
        workflow.TaskObject['Update Regions'].Execute()
        workflow.TaskObject['Add Boundary Layers'].Arguments.set_state(
            {r'LocalPrismPreferences': {r'Continuous': r'Stair Step'}}
        )
        workflow.TaskObject['Generate the Volume Mesh'].Execute()

class FluentSolver:
    """Handles solver operations in Fluent."""
    def __init__(self, session, is_solver_mode=False):
            if is_solver_mode:
                self.solver = session  # already in solver mode
            else:
                self.solver = self.initialize_solver(session)
    # def __init__(self, meshing_session):
    #     self.solver = self.initialize_solver(meshing_session)

    @staticmethod
    def initialize_solver(meshing_session):
        """Switch to the solver session and initialize settings."""
        solver = meshing_session.switch_to_solver()
        solver.mesh.check()
        solver.settings.setup.general.operating_conditions.gravity.enable = True
        solver.settings.setup.general.operating_conditions.gravity.components = [0.0, -9.81, 0.0]
        solver.setup.models.energy = {'enabled': True}
        solver.settings.setup.materials.database.copy_by_name(type="fluid", name="water-liquid")
        solver.settings.setup.cell_zone_conditions.fluid()

         # Setup turbulence model
        solver.settings.setup.models.viscous.model = "k-epsilon"
        solver.settings.setup.models.viscous.k_epsilon_model = "realizable" 
        return solver

    def set_velocity_inlet(self, inlet_name, velocity, temperature):
        """Set velocity inlet boundary conditions."""
        self.solver.settings.setup.boundary_conditions.velocity_inlet[inlet_name](
            momentum={
                'velocity_magnitude': {'option': 'value', 'value': velocity}
            },
            thermal={
                'temperature': {'option': 'value', 'value': temperature}
            },
        )

    def initialize_and_run(self, iterations):
        """Initialize the solver and run calculations."""
        self.solver.solution.initialization.hybrid_initialize()
        self.solver.settings.solution.run_calculation.iter_count = iterations
        self.solver.settings.solution.run_calculation.iterate()

    def set_turbulence_model(self, model_type, sub_model=None):
        """Set turbulence model using a dictionary-style assignment."""
        if model_type == "k-epsilon":
            self.solver.setup.models.viscous = {
                "model": "k-epsilon",
                "k_epsilon_model": sub_model or "realizable"
            }
        elif model_type == "k-omega":
            self.solver.setup.models.viscous = {
                "model": "k-omega",
                "k_omega_model": sub_model or "sst"
            }
        else:
            self.solver.setup.models.viscous = {
                "model": model_type
            }


class FluentPostProcessor:
    """Handles post-processing operations in Fluent."""

    def __init__(self, solver, output_folder):
        self.solver = solver
        self.output_folder = output_folder

    def create_and_save_contour(self, name, field, surfaces_list, file_name):
        """Create, display, and save a contour plot."""
        self.solver.settings.results.graphics.contour.create(name)
        self.solver.settings.results.graphics.contour[name](
            field=field,
            surfaces_list=surfaces_list
            #surfaces=surfaces_list
        )
        self.solver.settings.results.graphics.contour[name].display()
        self.solver.settings.results.graphics.views.auto_scale()
        # file_path = os.path.join(self.output_folder, file_name)
        file_path = os.path.abspath(os.path.join(self.output_folder, file_name))
        self.solver.settings.results.graphics.picture.save_picture(file_name=file_path)

    def create_plane_slice(self, name, origin, normal):
        """Create a plane slice."""
        self.solver.results.surfaces.plane_slice.create(
            name=name,
            normal=normal,
            distance_from_origin=origin
        )

    # def create_plane_slice(self, name, origin, normal):
    #     """Create a plane slice with specified origin and normal."""
    #     self.solver.results.surfaces.plane_slice.create(name)
    #     self.solver.results.surfaces.plane_slice[name].Arguments.set_state({
    #         "origin": origin,
    #         "normal": normal
    #     })

    def create_and_save_vector(self, name, field, surfaces_list, file_name):
        """Create, display, and save a vector plot."""
        # file_path = os.path.join(self.output_folder, file_name)
        file_path = os.path.abspath(os.path.join(self.output_folder, file_name))
        graphics = self.solver.settings.results.graphics
        graphics.vector[name] = {}
        vector = graphics.vector[name]
        vector.field = field
        vector.surfaces_list = surfaces_list
        vector.style = "arrow"
        vector.display()
        graphics.views.restore_view(view_name="right")
        graphics.views.auto_scale()
        graphics.picture.save_picture(file_name=file_path)

def load_inputs(yaml_path="input.yaml"):
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def normalize_path(path):
    return path.replace("\\", "/")

def get_latest_output_folder(base_dir=".", exclude_folder=None):
    """
    Returns the absolute path to the most recently created output_* folder,
    optionally excluding a specific folder.
    """
    folders = [
        f for f in os.listdir(base_dir)
        if f.startswith("output_") and os.path.isdir(os.path.join(base_dir, f))
    ]
    if not folders:
        raise FileNotFoundError("No output folders found.")

    sorted_folders = sorted(
        folders,
        key=lambda x: os.path.getctime(os.path.join(base_dir, x)),
        reverse=True
    )

    for folder in sorted_folders:
        abs_path = os.path.abspath(os.path.join(base_dir, folder))
        if abs_path != exclude_folder:
            return abs_path

    raise FileNotFoundError("No valid previous output folder found for rerun.")


def reload_case_from_folder(latest_folder, output_folder):
    """
    Loads the latest .cas.h5 file from the specified folder into Fluent,
    and returns the solver and case path.
    """
    cas_files = [f for f in os.listdir(latest_folder) if f.endswith(".cas.h5")]
    if not cas_files:
        raise FileNotFoundError("No .cas.h5 file found in the specified folder.")

    cas_filename = cas_files[0]
    case_path = os.path.join(latest_folder, cas_filename)

    session = pyfluent.launch_fluent(
        show_gui=True,
        mode="solver",
        precision="double",
        processor_count=4,
        additional_arguments="-driver opengl"
    )
    session.file.read_case(file_name=os.path.abspath(case_path))

    solver = FluentSolver(session, True)
    case_path = os.path.join(output_folder, cas_filename)
    return solver, case_path

def run():

# Create output folder with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = os.path.abspath(f"output_{timestamp}")
    os.makedirs(output_folder, exist_ok=True)

    # Load simulation inputs from input.yaml
    inputs = load_inputs()
    

    inlet_settings = inputs["velocity_inlets"]
    iterations = inputs["iterations"]
    geometry_path = inputs["geometry_file"]

    post_settings = inputs["post_processing"]
    geometry_basename = os.path.splitext(os.path.basename(geometry_path))[0]
    case_filename = f"{geometry_basename}.cas.h5"
    case_path = os.path.abspath(os.path.join(output_folder, case_filename))
    # geometry_basename = os.path.splitext(os.path.basename(geometry_path))[0]
    # case_path = os.path.abspath(os.path.join(output_folder, case_filename))
    # case_filename = f"{geometry_basename}.cas.h5"

    if  inputs.get("rerun_case", False):
        print("Rerunning the latest case...")
        # os.makedirs(output_folder, exist_ok=True)
        latest_folder = get_latest_output_folder(exclude_folder=output_folder)
        solver, case_path = reload_case_from_folder(latest_folder, output_folder)
    # Meshings
    else:
        
        print("Running a new case...")
        # os.makedirs(output_folder, exist_ok=True)
        meshing = FluentMeshing()
        meshing.import_geometry(geometry_path)
        meshing.setup_meshing()

        # Solver
        solver = FluentSolver(meshing.session)

    # Set velocity inlet boundary conditions
    for inlet in inlet_settings:
        solver.set_velocity_inlet(
            inlet_name=inlet["inlet_name"],
            velocity=inlet["velocity"],
            temperature=inlet["temperature"]
        )

    solver.initialize_and_run(iterations)

    # Post-processing
    post_processor = FluentPostProcessor(solver.solver, output_folder)

    post_processor.create_plane_slice(
        name=post_settings["create_plane_slice"]["name"],
        origin=post_settings["create_plane_slice"]["origin"],
        normal=post_settings["create_plane_slice"]["normal"]
    )

    # post_processor.create_and_save_contour(
    #     name=post_settings["create_contour"]["name"],
    #     field=post_settings["create_contour"]["field"],
    #     surfaces_list=post_settings["create_contour"]["surfaces"],
    #     file_name=post_settings["create_contour"]["file_name"]
    # )
    for contour in post_settings["create_contours"]:
        post_processor.create_and_save_contour(
            name=contour["name"],
            field=contour["field"],
            surfaces_list=contour["surfaces"],
            file_name=contour["file_name"]
        )

    post_processor.create_and_save_vector(
        name=post_settings["create_vector"]["name"],
        field=post_settings["create_vector"]["field"],
        surfaces_list=post_settings["create_vector"]["surfaces"],
        file_name=post_settings["create_vector"]["file_name"]
    )

   
    # ✅ Write the case file
    solver.solver.file.write_case(file_name=case_path)
    print(f"✅ Fluent case file saved: {case_path}")

    input("Press Enter to exit and close Fluent session...")
if __name__ == "__main__":
    run()
