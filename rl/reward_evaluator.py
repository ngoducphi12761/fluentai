# fluentai/rl/reward_evaluator.py
import numpy as np

def evaluate_auto_reward(result):
    """
    Automatically calculates reward based on simulation metrics.
    
    Args:
        result (dict): Simulation result dictionary containing:
            - converged (bool): Whether the simulation converged.
            - iterations (int): Number of iterations to converge.
            - mesh_skewness (float): Mesh skewness value.
            - runtime (float): Time taken for the simulation (seconds).

    Returns:
        float: Auto-calculated reward value.
    """
    if not result.get("converged", False):
        return -1.0  # Negative reward for non-convergence
    
    # Reward scaling
    convergence_score = max(1.0 - result.get("iterations", 1000) / 1000.0, 0.0)
    mesh_quality_score = max(1.0 - result.get("mesh_skewness", 1.0), 0.0)
    runtime_penalty = -0.001 * result.get("runtime", 100)  # Minor penalty for long runtime
    
    # Total reward
    auto_reward = convergence_score + mesh_quality_score + runtime_penalty
    return round(auto_reward, 3)

def get_user_feedback():
    """
    Prompts user for feedback on the mesh quality.
    
    Returns:
        float: +1 for yes, -1 for no, 0 for skip.
    """
    response = input("👤 Was the mesh appropriate? (y/n) [Enter to skip]: ").lower()
    return +1 if response == 'y' else -1 if response == 'n' else 0

def evaluate_total_reward(result, use_feedback=True):
    """
    Evaluates the total reward, combining auto-reward and user feedback.

    Args:
        result (dict): Simulation result dictionary.
        use_feedback (bool): Whether to include user feedback.

    Returns:
        float: Total reward value.
    """
    auto_reward = evaluate_auto_reward(result)
    user_reward = get_user_feedback() if use_feedback else 0

    total_reward = auto_reward + user_reward
    return round(total_reward, 3)
