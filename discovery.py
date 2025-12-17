# discovery.py

import socket
import threading
import time
from protocol import encode_hello, decode_message

DISCOVERY_PORT = 50000
BROADCAST_ADDR = ("255.255.255.255", DISCOVERY_PORT)


class PeerDiscovery:
    def __init__(self, peer_id: str, listen_port: int):
        self.peer_id = peer_id
        self.listen_port = listen_port
        self.peers = {}  # peer_id -> (ip, port)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Allow multiple peers on same machine (Windows-safe)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Enable broadcast
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.socket.bind(("0.0.0.0", DISCOVERY_PORT))


        self.running = True

    def start(self):
        threading.Thread(target=self._broadcast_loop, daemon=True).start()
        threading.Thread(target=self._listen_loop, daemon=True).start()

    def _broadcast_loop(self):
        while self.running:
            msg = encode_hello(self.peer_id, self.listen_port)
            self.socket.sendto(msg, BROADCAST_ADDR)
            time.sleep(2)

    def _listen_loop(self):
        while self.running:
            data, addr = self.socket.recvfrom(1024)
            msg_type, fields = decode_message(data)

            if msg_type != "HELLO":
                continue

            peer_id, port = fields
            port = int(port)

            # Ignore self
            if peer_id == self.peer_id:
                continue

            self.peers[peer_id] = (addr[0], port)
            print(f"[DISCOVERY] Found peer {peer_id} at {addr[0]}:{port}")

    def get_peers(self):
        return dict(self.peers)
