# fluentai/rl/feedback_logger.py
import json

def log_feedback(state, action, reward, log_path):
    entry = {"state": state, "action": action, "reward": reward}
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")
# fluentai/rl/feedback_logger.py
import json
import os
from datetime import datetime

LOG_PATH = "rl/logs/feedback_log.jsonl"

def initialize_logger():
    """Ensure log directory exists."""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def log_feedback(state, action, reward):
    """
    Logs state, action, and reward as a single JSON entry.

    Args:
        state (dict): The CFD problem state (geometry, Re, flow type).
        action (dict): The selected action (mesh type, sizing, etc.).
        reward (float): The reward value assigned to this action.
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "state": state,
        "action": action,
        "reward": reward
    }

    with open(LOG_PATH, "a") as log_file:
        log_file.write(json.dumps(entry) + "\n")

def read_feedback_logs():
    """
    Reads and returns all feedback logs.

    Returns:
        list: A list of feedback entries.
    """
    if not os.path.exists(LOG_PATH):
        return []

    with open(LOG_PATH, "r") as log_file:
        logs = [json.loads(line) for line in log_file]
    return logs

def clear_feedback_logs():
    """
    Clears all feedback logs.
    """
    if os.path.exists(LOG_PATH):
        open(LOG_PATH, "w").close()
