import yaml

class YAMLEditor:
    def __init__(self, yaml_file="input.yaml"):
        self.yaml_file = yaml_file
        self.data = self.load_yaml()

    def load_yaml(self):
        """Load YAML file into memory."""
        with open(self.yaml_file, 'r') as f:
            return yaml.safe_load(f)

    def save_yaml(self):
        """Save current data back to YAML file."""
        with open(self.yaml_file, 'w') as f:
            yaml.dump(self.data, f, default_flow_style=False)

    def update_inlet_velocity(self, inlet_name, new_velocity, save=True):
        """Update velocity value for a specific inlet."""
        found = False
        for inlet in self.data.get("velocity_inlets", []):
            if inlet["inlet_name"].strip() == inlet_name.strip():
                inlet["velocity"] = new_velocity
                found = True
                break

        if not found:
            raise ValueError(f"Inlet '{inlet_name}' not found in velocity_inlets.")

        if save:
            self.save_yaml()
        print(f"✅ Updated {inlet_name} velocity to {new_velocity} m/s")

    def update_inlet_temperature(self, inlet_name, new_temperature, save=True):
        """Update temperature value for a specific inlet."""
        found = False
        for inlet in self.data.get("velocity_inlets", []):
            if inlet["inlet_name"].strip() == inlet_name.strip():
                inlet["temperature"] = new_temperature
                found = True
                break

        if not found:
            raise ValueError(f"Inlet '{inlet_name}' not found in velocity_inlets.")

        if save:
            self.save_yaml()
        print(f"✅ Updated {inlet_name} temperature to {new_temperature} K")

    def update_all_inlet_velocities(self, new_velocity, save=True):
        """Update velocity value for all inlets."""
        if "velocity_inlets" in self.data:
            for inlet in self.data["velocity_inlets"]:
                inlet["velocity"] = new_velocity

            if save:
                self.save_yaml()
            print(f"✅ Updated all inlets to velocity {new_velocity} m/s")
        else:
            raise ValueError("No 'velocity_inlets' section found in input.yaml.")

    def update_turbulence_model(self, model_name, save=True):
        """Update the turbulence model setting."""
        self.data["turbulence_model"] = model_name
        if save:
            self.save_yaml()
        print(f"✅ Set turbulence model to {model_name}")

    def update_iterations(self, iteration_count, save=True):
        """Update number of solver iterations."""
        self.data["iterations"] = iteration_count
        if save:
            self.save_yaml()
        print(f"✅ Set iterations to {iteration_count}")

# Example usage
if __name__ == "__main__":
    editor = YAMLEditor("input.yaml")
    editor.update_inlet_velocity("velocity-inlet-1", 3.0)
    editor.update_inlet_temperature("velocity-inlet-1", 350.0)
    editor.update_turbulence_model("k-epsilon")
    editor.update_iterations(500)
