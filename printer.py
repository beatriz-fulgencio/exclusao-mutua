import time

# Function to print a sequence of numbers with a delay
def print_sequence(start, count, node_id):
    """
    Prints a sequence of numbers starting from 'start' with a total of 'count' numbers.
    Each number is prefixed with the node ID and printed with a delay of 0.5 seconds.

    Args:
        start (int): The starting number of the sequence.
        count (int): The total number of numbers to print.
        node_id (int): The ID of the node printing the sequence.
    """
    for i in range(count):
        # Print the current number in the sequence with the node ID
        print(f"[NODE {node_id}] {start + i}")
        # Pause for 0.5 seconds before printing the next number
        time.sleep(0.5)
