import json
import threading
import time
import sys

from mutual_exclusion import RicartAgrawala
from network import ServerThread, send_message
from printer import print_sequence
from utils import random_access_decision, random_sequence_length

class Node:
    
    def __init__(self, node_id, config_path='config.json'):
        # Initialize the node with its ID and configuration file
        self.node_id = node_id
        self.nodes = self.load_config(config_path)
        print(f"Node {self.node_id} initialized with config: {self.nodes}", flush=True)                        

        # Get the current node's configuration
        self.me = next(n for n in self.nodes if n["id"] == self.node_id)
        # Initialize the Ricart-Agrawala mutual exclusion algorithm
        self.ricart = RicartAgrawala(node_id, self.nodes)
        self.last_timestamp = 0

        # Start the server thread to listen for incoming messages
        self.server = ServerThread(self.me['host'], self.me['port'], self.handle_message)
        self.server.start()

    def load_config(self, path):
        """
        Loads the configuration file containing the list of nodes.
        
        Args:
            path (str): The path to the configuration file.
        """
        
        # Load the configuration file containing the list of nodes
        with open(path) as f:
            return json.load(f)["nodes"]

    def handle_message(self, message):
        """
        Handles an incoming message from another node.
        
        Args:
            message (dict): The message received from the other node.
        """
        # Handle incoming messages based on their type
        msg_type = message["type"]
        if msg_type == "request":
            # Handle a critical section request
            ts = message["timestamp"]
            sender = message["id"]
            if self.ricart.receive_request(ts, sender):
                self.send_ok(sender)
        elif msg_type == "ok":
            # Handle an "ok" message
            self.ricart.receive_ok(message["id"])

    def send_ok(self, target_id):
        """
        Sends an "ok" message to the specified node.    
        
        Args:
            target_id (int): The ID of the node to send the message to.        
        """
        # Send an "ok" message to the specified node
        node = next(n for n in self.nodes if n["id"] == target_id)
        send_message(node["host"], node["port"], {"type": "ok", "id": self.node_id})

    def request_cs(self):
        """
        Requests access to the critical section by sending request messages to all other nodes.
        """
        # Request access to the critical section
        ts = self.ricart.request_access()
        self.last_timestamp = max(self.last_timestamp, ts)
        for n in self.nodes:
            if n["id"] != self.node_id:
                # Send a request message to all other nodes
                send_message(n["host"], n["port"], {"type": "request", "timestamp": ts, "id": self.node_id})

    def run(self):
        """
        Main loop for the node. The node periodically decides whether to request access to the critical section.
        If access is granted, it performs operations in the critical section.
        
        The node also listens for incoming messages using a separate server thread.
        """
        # Main loop for the node
        while True:
            time.sleep(2)  # Wait for a random interval
            if random_access_decision():
                # Decide whether to request access to the critical section
                self.request_cs()
                while not self.ricart.can_enter_cs():
                    # Wait until access to the critical section is granted
                    time.sleep(0.1)
                try:
                    # Perform operations in the critical section
                    k = random_sequence_length()
                    print_sequence(self.last_timestamp, k, self.node_id)
                    self.last_timestamp += k
                    # Release access to the critical section
                    deferred = self.ricart.release_access()
                    for pid in deferred:
                        # Send "ok" messages to deferred requests
                        self.send_ok(pid)
                except Exception as e:
                    # Handle any errors in the critical section
                    print("Error in critical section:", e)

if __name__ == "__main__":
    # Entry point for the script
    if len(sys.argv) != 2:
        print("Usage: python node.py <node_id>")
        sys.exit(1)
    # Initialize and run the node
    node = Node(int(sys.argv[1]))
    node.run()
