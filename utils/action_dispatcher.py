from yamleditor import YAMLEditor

def execute_action_plan(action_plan: list):
    """
    Execute all actions from Action Plan to modify input.yaml.
    """
    yaml_editor = YAMLEditor("input.yaml")

    for action in action_plan:
        action_type = action.get("action")
        parameters = action.get("parameters", {})

        if action_type == "update_inlet_velocity":
            inlet_name = parameters.get("inlet_name")
            velocity = parameters.get("velocity")
            yaml_editor.update_inlet_velocity(inlet_name, velocity, save=False)

        elif action_type == "update_inlet_temperature":
            inlet_name = parameters.get("inlet_name")
            temperature = parameters.get("temperature")
            yaml_editor.update_inlet_temperature(inlet_name, temperature, save=False)

        elif action_type == "update_all_inlet_velocities":
            velocity = parameters.get("velocity")
            yaml_editor.update_all_inlet_velocities(velocity, save=False)

        elif action_type == "update_turbulence_model":
            model = parameters.get("model")
            yaml_editor.update_turbulence_model(model, save=False)

        elif action_type == "update_iterations":
            iteration_count = parameters.get("iterations")
            yaml_editor.update_iterations(iteration_count, save=False)

        elif action_type == "rerun_simulation":
            rerun = parameters.get("rerun")
            yaml_editor.toggle_rerun_case(rerun, save=False)

        else:
            print(f"⚠️ Warning: Unknown action type '{action_type}' — skipping.")

    # 🔥 Save all changes once at the end
    yaml_editor.save_yaml()
    print("✅ All actions ./ and YAML saved successfully.")
