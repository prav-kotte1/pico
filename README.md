# Reliable UDP-based Peer-to-Peer File Transfer System

## Overview
This project implements a **peer-to-peer (P2P) file transfer system over UDP**, designed to work reliably despite UDP’s lack of delivery guarantees.  
Peers automatically discover each other on a local network and can request files using a simple command-line interface (CLI).

The project focuses on **networking fundamentals, application-layer reliability, concurrency, and distributed systems concepts**, making it suitable for SDE and Data Engineering interviews.


## Key Features
- Peer discovery over LAN using **UDP broadcast**
- Reliable file transfer over **UDP**
  - File chunking
  - Sequence numbers
  - ACK-based retransmission
- Concurrent sender and receiver architecture
- Simple and interactive **CLI**
- Windows-safe socket handling


## Architecture

```text
Peer
 ├── Discovery Service (UDP Broadcast)
 ├── Receiver Thread (blocking UDP socket)
 ├── Sender Logic (timeout-based UDP socket)
 └── Command-Line Interface
```

Each peer acts as both a **client** (requesting files) and a **server** (serving files).  
No centralized server is required.



## Protocol Design

### Message Types

| Message | Purpose |
|-------|---------|
| HELLO | Peer discovery |
| DATA | File chunk transfer |
| ACK | Chunk acknowledgement |
| FILES | Local file listing |


### Chunking and Sequencing
- Files are split into **fixed-size chunks (1024 bytes)**
- Each chunk is assigned a **sequence number**
- Sequence numbers allow:
  - Correct ordering
  - Detection of missing packets



### Reliability Mechanism
Since UDP does not guarantee delivery:
- The sender transmits one chunk at a time
- The receiver sends an ACK for each chunk
- If an ACK is not received within a timeout, the chunk is retransmitted

This implements **application-layer reliability**, conceptually similar to TCP but intentionally simplified.


## Concurrency Model
To avoid race conditions and socket conflicts:
- **Receiver socket**
  - Blocking
  - Dedicated to listening for incoming data
- **Sender socket**
  - Timeout-enabled
  - Dedicated to sending data and receiving ACKs

Using separate sockets ensures clean concurrency and avoids timeout interference between threads.


## Command-Line Interface (CLI)

Available commands:
```text
list                # List discovered peers
files               # List local shared files
get <filename>      # Request a file from a peer
```
