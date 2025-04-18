import os
import ansys.fluent.core as pyfluent


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

    def __init__(self, meshing_session):
        self.solver = self.initialize_solver(meshing_session)

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


class FluentPostProcessor:
    """Handles post-processing operations in Fluent."""

    def __init__(self, solver):
        self.solver = solver

    def create_and_save_contour(self, name, field, surfaces_list, file_name):
        """Create, display, and save a contour plot."""
        self.solver.settings.results.graphics.contour.create(name)
        self.solver.settings.results.graphics.contour[name](
            field=field,
            surfaces_list=surfaces_list
        )
        self.solver.settings.results.graphics.contour[name].display()
        self.solver.settings.results.graphics.views.auto_scale()
        self.solver.settings.results.graphics.picture.save_picture(file_name=file_name)

    def create_plane_slice(self, name, origin, normal):
        """Create a plane slice."""
        self.solver.results.surfaces.plane_slice.create(
            name=name,
            origin=origin,
            normal=normal
        )

    def create_and_save_vector(self, name, field, surfaces_list, file_name):
        """Create, display, and save a vector plot."""
        graphics = self.solver.settings.results.graphics
        graphics.vector[name] = {}
        vector = graphics.vector[name]
        vector.field = field
        vector.surfaces_list = surfaces_list
        vector.style = "arrow"
        vector.display()
        graphics.views.restore_view(view_name="right")
        graphics.views.auto_scale()
        graphics.picture.save_picture(file_name=file_name)


def main():
    # Constants
    inlet_velocity = 2.0
    inlet_1_name = "velocity-inlet-1"
    inlet_2_name = "velocity-inlet-2"
    temperature = 300.0
    iterations = 200
    geometry_file = "Static Mixer geometry.dsco"
    geometry_path = os.path.join("geometry", geometry_file)

    # Meshing
    meshing = FluentMeshing()
    meshing.import_geometry(geometry_path)
    meshing.setup_meshing()

    # Solver
    solver = FluentSolver(meshing.session)
    solver.set_velocity_inlet(inlet_1_name, inlet_velocity, temperature)
    solver.set_velocity_inlet(inlet_2_name, inlet_velocity, temperature)
    solver.initialize_and_run(iterations)

    # Post-processing
    post_processor = FluentPostProcessor(solver.solver)
    post_processor.create_and_save_contour(
        "velocity_contour", "velocity-magnitude", ["pressure-outlet"], "velocity.png"
    )
    post_processor.create_and_save_contour(
        "temperature_contour", "temperature", ["pressure-outlet"], "temperature.png"
    )
    post_processor.create_plane_slice("center_yz_plane", origin=[0.0, 0.0, 0.0], normal=[1.0, 0.0, 0.0])
    post_processor.create_and_save_contour(
        "yz_plane_velocity", "velocity-magnitude", ["center_yz_plane"], "yz_plane_velocity.png"
    )
    post_processor.create_and_save_vector(
        "velocity_yz_plane", "velocity-magnitude", ["center_yz_plane"], "velocity_yz_plane.png"
    )

    # Keep the script alive interactively
    input("Press Enter to exit and close Fluent session...")


if __name__ == "__main__":
    main()