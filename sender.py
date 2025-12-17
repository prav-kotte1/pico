# sender.py

import socket
import time
from protocol import encode_data, encode_ack, decode_ack

CHUNK_SIZE = 4
ACK_TIMEOUT = 0.5


class FileSender:
    def __init__(self, sock: socket.socket, peer_addr):
        self.sock = sock
        self.peer_addr = peer_addr

    def send_file(self, filepath: str):
        filename = filepath.split("/")[-1]

        with open(filepath, "rb") as f:
            seq = 0
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break

                packet = encode_data(filename, seq, chunk)

                while True:
                    self.sock.sendto(packet, self.peer_addr)
                    self.sock.settimeout(ACK_TIMEOUT)


                    try:
                        data, _ = self.sock.recvfrom(1024)
                        ack_file, ack_seq = decode_ack(data)

                        if ack_file == filename and ack_seq == seq:
                            break
                    except socket.timeout:
                        print(f"[RETRY] seq {seq}")

                seq += 1

        print("[SENDER] File transfer complete")
