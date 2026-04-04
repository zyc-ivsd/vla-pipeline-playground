# agent.py

def decide_action(objects):
    """
    objects: list[str]
    return: str
    """
    if "bottle" in objects:
        return "pick_bottle"
    elif "person" in objects:
        return "follow_person"
    else:
        return "idle"