# receiver.py

import socket
import os
from protocol import decode_data, encode_ack

class FileReceiver:
    def __init__(self, sock: socket.socket, save_dir="files"):
        self.sock = sock
        self.save_dir = save_dir
        self.buffers = {}  # filename -> {seq: data}

        os.makedirs(self.save_dir, exist_ok=True)

    def listen(self):
        while True:
            packet, addr = self.sock.recvfrom(2048)

            if packet.startswith(b"DATA"):
                filename, seq, chunk = decode_data(packet)

                if filename not in self.buffers:
                    self.buffers[filename] = {}

                self.buffers[filename][seq] = chunk

                ack = encode_ack(filename, seq)
                self.sock.sendto(ack, addr)

                print(f"[RECEIVED] {filename} seq={seq}")

                # TEMP heuristic: save immediately for now
                self._save_file(filename)

    def _save_file(self, filename):
        chunks = self.buffers[filename]
        path = os.path.join(self.save_dir, f"received_{filename}")

        with open(path, "wb") as f:
            for seq in sorted(chunks):
                f.write(chunks[seq])

        print(f"[SAVED] {path}")
