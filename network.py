import socket
import threading
import json
import time

class ServerThread(threading.Thread):
    def __init__(self, host, port, handler):
        super().__init__()
        self.host = host
        self.port = port
        self.handler = handler
        self.daemon = True

    def run(self):
        """
        Starts the server and listens for incoming connections.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            print(f"[Node {self.port}] Listening on {self.host}:{self.port}", flush=True)
            s.listen()
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self, conn):
        """
        Handles incoming messages from a client.        
        """
        with conn:
            data = conn.recv(1024)
            if data:
                message = json.loads(data.decode())
                self.handler(message)

def send_message(host, port, message, retries=3, delay=1):
    """
    Sends a message to the specified host and port with retry logic.

    Args:
        host (str): The target host.
        port (int): The target port.
        message (dict): The message to send.
        retries (int): Number of retry attempts.
        delay (int): Delay (in seconds) between retries.
    """
    for attempt in range(retries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(json.dumps(message).encode())
                return  # Exit the function if the message is sent successfully
        except Exception as e:
            print(f"[ERROR] Attempt {attempt + 1}/{retries} — Could not send to {host}:{port} — {e}", flush=True)
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                print(f"[ERROR] Failed to send message to {host}:{port} after {retries} attempts.", flush=True)
                raise