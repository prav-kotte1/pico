# test_sender.py
import socket
from sender import FileSender

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender = FileSender(sock, ("127.0.0.1", 6000))

sender.send_file("files/test.txt")
