def is_action_command(user_query: str) -> bool:
    """
    Detect if the user query is an action-type command (needs JSON Action Plan),
    or a general question (needs natural answer).
    """
    action_keywords = [
        "set", "update", "change", "switch", 
        "run", "configure", "assign", "modify",
        "execute the simulation", "start the simulation",
        "make it run", "launch the solver",
        "rerun the simulation", "rerun simulation"
    ]

    user_query_lower = user_query.lower()
    
    return any(keyword in user_query_lower for keyword in action_keywords)
