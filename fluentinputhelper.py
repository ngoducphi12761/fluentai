import yaml

class FluentInputHelper:
    """Class to load, validate, and assist with Fluent simulation input YAML files."""

    def __init__(self, yaml_path="input.yaml"):
        self.yaml_path = yaml_path
        self.data = self.load_and_validate()

    def load_and_validate(self):
        """Load YAML input file and validate its contents."""
        with open(self.yaml_path, 'r') as f:
            data = yaml.safe_load(f)

        # Validation logic
        mandatory_keys = ["velocity_inlets", "iterations", "geometry_file", "post_processing"]
        for key in mandatory_keys:
            if key not in data:
                raise ValueError(f"❌ Missing key '{key}' in {self.yaml_path}")

        # Validate velocity_inlets
        for inlet in data["velocity_inlets"]:
            if "inlet_name" not in inlet or "velocity" not in inlet or "temperature" not in inlet:
                raise ValueError(f"❌ Each velocity_inlet must have 'inlet_name', 'velocity', and 'temperature'.")
            if inlet["velocity"] <= 0:
                raise ValueError(f"❌ Velocity must be positive for inlet '{inlet.get('inlet_name', 'unknown')}'.")
            if inlet["temperature"] <= 0:
                raise ValueError(f"❌ Temperature must be positive for inlet '{inlet.get('inlet_name', 'unknown')}'.")

        # Validate iterations
        if data["iterations"] <= 0:
            raise ValueError("❌ Iterations must be a positive number.")

        # Validate post-processing sections
        required_post_keys = ["create_plane_slice", "create_contour", "create_vector"]
        for key in required_post_keys:
            if key not in data["post_processing"]:
                raise ValueError(f"❌ Missing post-processing config: '{key}'")

        print(f"✅ {self.yaml_path} validated successfully.")
        return data

    def get_data(self):
        """Return the validated input data."""
        return self.data
