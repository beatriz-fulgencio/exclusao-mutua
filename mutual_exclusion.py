import threading

class RicartAgrawala:
    def __init__(self, node_id, nodes):
        """
        Initialize the Ricart-Agrawala algorithm instance.

        Args:
            node_id (int): The ID of the current node.
            nodes (list): List of all node IDs in the distributed system.
        """
        self.node_id = node_id  # ID of the current node
        self.nodes = nodes  # List of all nodes in the system
        self.timestamp = 0  # Logical clock timestamp
        self.requesting = False  # Whether the node is requesting access to the critical section
        self.deferred_replies = []  # List of nodes whose replies are deferred
        self.ok_received = set()  # Set of nodes from which OK messages have been received
        self.lock = threading.RLock()  # Reentrant lock for thread safety
        self.failed_nodes = set()
        

    def increment_clock(self):
        """
        Increment the logical clock and return the updated timestamp.

        Returns:
            int: The updated timestamp.
        """
        with self.lock:
            self.timestamp += 1
            return self.timestamp

    def receive_request(self, timestamp, sender_id):
        """
        Handle an incoming request for critical section access.

        Args:
            timestamp (int): The logical clock timestamp of the sender.
            sender_id (int): The ID of the sender node.

        Returns:
            bool: True if an OK message should be sent, False if the reply is deferred.
        """
        with self.lock:
            # Update the logical clock
            self.timestamp = max(self.timestamp, timestamp) + 1
            # Determine whether to send OK or defer the reply
            if (not self.requesting or
                (timestamp, sender_id) < (self.timestamp, self.node_id)):
                return True  # Send OK
            else:
                self.deferred_replies.append(sender_id)  # Defer the reply
                return False  # Delay response

    def receive_ok(self, sender_id):
        """
        Handle an incoming OK message.

        Args:
            sender_id (int): The ID of the sender node.
        """
        with self.lock:
            self.ok_received.add(sender_id)  # Add sender to the set of OK received

    def request_access(self):
        """
        Request access to the critical section.

        Returns:
            int: The updated logical clock timestamp.
        """
        with self.lock:
            self.requesting = True  # Mark as requesting access
            self.ok_received.clear()  # Clear previous OK messages
            self.increment_clock()  # Increment the logical clock
            print(f"[Node {self.node_id}] Requesting access with timestamp {self.timestamp}", flush=True)
            return self.timestamp

    def can_enter_cs(self):
        """
        Check if the node can enter the critical section.

        Returns:
            bool: True if all necessary OK messages have been received, False otherwise.
        """
        with self.lock:
            return len(self.ok_received) == len(self.nodes) - 1

    def wait_for_ok_responses(self, timeout=3):
        import time
        start_time = time.time()
        while True:
            with self.lock:
                expected = [n["id"] for n in self.nodes if n["id"] != self.node_id and n["id"] not in self.failed_nodes]
                if all(pid in self.ok_received for pid in expected):
                    return True
            if time.time() - start_time > timeout:
                with self.lock:
                    for n in self.nodes:
                        if n["id"] != self.node_id and n["id"] not in self.ok_received:
                            self.failed_nodes.add(n["id"])
                            print(f"[Node {self.node_id}] Timeout: assuming node {n['id']} has failed", flush=True)
                return True
            time.sleep(0.1)


    def release_access(self):
        """
        Release access to the critical section and send deferred replies.

        Returns:
            list: List of nodes to which deferred replies should be sent.
        """
        with self.lock:
            self.requesting = False  # Mark as not requesting access
            replies = list(self.deferred_replies)  # Copy deferred replies
            self.deferred_replies.clear()  # Clear deferred replies
            return replies
