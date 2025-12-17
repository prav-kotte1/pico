# peer.py

import socket
import uuid
import threading
import os

from discovery import PeerDiscovery
from sender import FileSender
from receiver import FileReceiver

DATA_PORT = 6000         # CHANGE to 6001 in second peer
FILES_DIR = "files"


def main():
    peer_id = str(uuid.uuid4())[:8]

    # ---------------------------
    # Receiver socket (BLOCKING)
    # ---------------------------
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_sock.bind(("0.0.0.0", DATA_PORT))

    receiver = FileReceiver(recv_sock, FILES_DIR)

    # ---------------------------
    # Sender socket (TIMEOUT)
    # ---------------------------
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ---------------------------
    # Peer discovery
    # ---------------------------
    discovery = PeerDiscovery(peer_id, DATA_PORT)
    discovery.start()

    # ---------------------------
    # Start receiver thread
    # ---------------------------
    threading.Thread(
        target=receiver.listen,
        daemon=True
    ).start()

    print(f"[STARTED] Peer ID: {peer_id} | Listening on port {DATA_PORT}")

    # ---------------------------
    # CLI loop
    # ---------------------------
    while True:
        cmd = input("p2p> ").strip()

        if cmd == "list":
            peers = discovery.get_peers()
            if not peers:
                print("No peers discovered")
            else:
                for pid, addr in peers.items():
                    print(f"{pid} -> {addr}")

        elif cmd == "files":
            if not os.path.exists(FILES_DIR):
                print("No files directory")
            else:
                files = os.listdir(FILES_DIR)
                print("Local files:", files)

        elif cmd.startswith("get "):
            _, filename = cmd.split(maxsplit=1)

            peers = discovery.get_peers()
            if not peers:
                print("No peers available")
                continue

            filepath = os.path.join(FILES_DIR, filename)
            if not os.path.exists(filepath):
                print(f"File not found: {filename}")
                continue

            peer_addr = list(peers.values())[0]  # pick first peer
            sender = FileSender(send_sock, peer_addr)
            sender.send_file(filepath)

        else:
            print("Commands: list | files | get <filename>")


if __name__ == "__main__":
    main()
