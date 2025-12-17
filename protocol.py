# protocol.py

def encode_hello(peer_id: str, listen_port: int) -> bytes:
    """
    HELLO|peer_id|listen_port
    """
    msg = f"HELLO|{peer_id}|{listen_port}"
    return msg.encode("utf-8")


def decode_message(data: bytes):
    """
    Returns (msg_type, fields_list)
    """
    try:
        text = data.decode("utf-8")
        parts = text.strip().split("|")
        return parts[0], parts[1:]
    except Exception:
        return None, None

# protocol.py (append)

def encode_data(filename: str, seq: int, chunk: bytes) -> bytes:
    header = f"DATA|{filename}|{seq}|{len(chunk)}\n"
    return header.encode("utf-8") + chunk


def decode_data(packet: bytes):
    header, payload = packet.split(b"\n", 1)
    parts = header.decode("utf-8").split("|")
    _, filename, seq, size = parts
    return filename, int(seq), payload


def encode_ack(filename: str, seq: int) -> bytes:
    msg = f"ACK|{filename}|{seq}"
    return msg.encode("utf-8")


def decode_ack(data: bytes):
    text = data.decode("utf-8")
    _, filename, seq = text.split("|")
    return filename, int(seq)

def encode_files(file_list):
    msg = "FILES|" + ",".join(file_list)
    return msg.encode("utf-8")


def decode_files(data: bytes):
    text = data.decode("utf-8")
    _, files = text.split("|", 1)
    return files.split(",") if files else []
