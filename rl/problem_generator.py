# fluentai/rl/problem_generator.py
import random

class ProblemGenerator:
    def __init__(self, seed=None):
        """
        Initializes the Problem Generator.
        
        Args:
            seed (int, optional): Random seed for reproducibility.
        """
        self.geometries = ["pipe", "duct", "mixer", "channel"]
        self.flow_types = ["laminar", "turbulent"]
        self.solvers = ["pressure-based", "density-based"]
        self.gradients = ["low", "medium", "high"]
        
        if seed:
            random.seed(seed)

    def generate_state(self):
        """
        Generates a random CFD problem state for RL training.

        Returns:
            dict: A dictionary representing the problem state.
        """
        state = {
            "geometry": random.choice(self.geometries),
            "flow_type": random.choice(self.flow_types),
            "Re": random.randint(1000, 100000),  # Random Reynolds number
            "solver": random.choice(self.solvers),
            "expected_gradients": random.choice(self.gradients),
            "domain_size": round(random.uniform(0.1, 5.0), 2),  # Domain size in meters
        }
        return state

    def generate_custom_state(self, geometry, flow_type, Re, solver, gradients, domain_size):
        """
        Generates a custom CFD problem state.

        Args:
            geometry (str): The type of geometry (pipe, duct, etc.)
            flow_type (str): Flow type (laminar, turbulent).
            Re (int): Reynolds number.
            solver (str): Solver type (pressure-based, density-based).
            gradients (str): Expected gradient levels (low, medium, high).
            domain_size (float): Size of the domain (meters).
        
        Returns:
            dict: A dictionary representing the custom problem state.
        """
        state = {
            "geometry": geometry,
            "flow_type": flow_type,
            "Re": Re,
            "solver": solver,
            "expected_gradients": gradients,
            "domain_size": domain_size
        }
        return state

    def generate_random_problem_set(self, num_problems=10):
        """
        Generates a set of random CFD problem states.

        Args:
            num_problems (int): Number of problems to generate.
        
        Returns:
            list: List of generated problem states.
        """
        return [self.generate_state() for _ in range(num_problems)]
