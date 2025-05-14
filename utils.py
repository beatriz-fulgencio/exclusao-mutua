import random

def random_access_decision():
    """
    Decides randomly whether to request access to the critical section.
    """
    return random.random() > 0.5

def random_sequence_length():
    """
    Generates a random sequence length between 1 and 10.
    """
    
    return random.randint(1, 10)
