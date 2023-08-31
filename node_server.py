import socket
import threading
import json
from bkc import Block, calculate_hash, proof_of_work, create_genesis_block, create_new_block, json_block_decoder

# Add other peer IPs as required
peer_nodes = ['127.0.0.1']

# Global variable for the blockchain list and peers
blockchain = [create_genesis_block()]

BASE_PORT = 5000  # Start from this port
MAX_NODES = 1000  # Arbitrarily chosen limit for this example
END_PORT = BASE_PORT + MAX_NODES  # We're allowing a maximum of 1000 nodes in this example

def find_available_port():
    for port in range(BASE_PORT, END_PORT):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Try to bind to the port
            # If already in use, the bind will raise an exception
            try:
                s.bind(('0.0.0.0', port))
                return port  # The port is available
            except socket.error:
                pass
    raise ValueError("No available ports in the range!")

def get_chain_from_peer(peer):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((peer, 5000))
    s.send(b'get_chain')
    return json.loads(s.recv(4096).decode(), object_hook=json_block_decoder)

def sync_chains(blockchain, peer_nodes):
    for peer in peer_nodes:
        peer_chain = get_chain_from_peer(peer)
        if len(peer_chain) > len(blockchain):
            blockchain = peer_chain
    return blockchain

def handle_client(blockchain, client_socket):
    request = client_socket.recv(1024).decode()
    if request == 'get_chain':
        client_socket.send(json.dumps(blockchain, default=lambda o: o.__dict__).encode())
    elif request == 'add_block':
        new_block_data = client_socket.recv(1024).decode()
        new_block = create_new_block(blockchain[-1], new_block_data)
        if new_block:
            blockchain.append(new_block)
            client_socket.send(b'Success')
        else:
            client_socket.send(b'Error: Unable to add block')
    client_socket.close()

def start_server(blockchain, port=find_available_port()):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[*] Listening on port {port}")
    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(blockchain, client))
        client_handler.start()


