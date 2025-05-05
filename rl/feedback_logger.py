# fluentai/rl/feedback_logger.py
import json

def log_feedback(state, action, reward, log_path):
    entry = {"state": state, "action": action, "reward": reward}
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")
