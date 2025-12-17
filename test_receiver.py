# test_receiver.py
import socket
from receiver import FileReceiver

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 6000))

receiver = FileReceiver(sock)
receiver.listen()
