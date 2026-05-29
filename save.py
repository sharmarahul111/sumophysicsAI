# save.py

import pickle

def save_agents(items, filename="saved.pkl"):
    """
    Saves a list of items to a pickle file.
    """
    with open(filename, "wb") as f:
        pickle.dump(items, f)


def load_agents(filename="saved.pkl"):
    """
    Loads and returns items from a pickle file.
    """
    with open(filename, "rb") as f:
        return pickle.load(f)