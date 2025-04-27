"""Communication file using socket."""

# NOTE: This file is mostly copied/referenced as it is far from our focus.

import logging
import pickle
import socket
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CommunicationHandler:
    def __init__(self, host: str = "localhost", port: int = 5000):
        self.host = host
        self.port = port
        self.socket = None
        self.connection = None

    def start_server(self):
        """Initialize server socket"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        logger.info(f"Server listening on {self.host}:{self.port}")

    def start_client(self):
        """Initialize client socket"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.connection = self.socket
        logger.info(f"Client connected to {self.host}:{self.port}")

    def accept_connection(self):
        """Accept incoming connection (server-side)"""
        self.connection, addr = self.socket.accept()
        logger.info(f"Accepted connection from {addr}")
        return addr

    def send_data(self, data: Any):
        """Send data over the connection"""
        serialized_data = pickle.dumps(data)
        # First send the length of the data
        self.connection.send(len(serialized_data).to_bytes(4, "big"))
        # Then send the data
        self.connection.send(serialized_data)
        logger.debug(f"Sent {len(serialized_data)} bytes")

    def receive_data(self) -> Any:
        """Receive data from the connection"""
        # First receive the length of the data
        data_length = int.from_bytes(self.connection.recv(4), "big")
        # Then receive the data
        data = b""
        while len(data) < data_length:
            packet = self.connection.recv(data_length - len(data))
            if not packet:
                raise ConnectionError("Connection broken")
            data += packet
        return pickle.loads(data)

    def close(self):
        """Close the connection"""
        if self.connection:
            self.connection.close()
        if self.socket:
            self.socket.close()
        logger.info("Connection closed")
