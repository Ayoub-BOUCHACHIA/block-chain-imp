import socket
import sys

def get_chain_from_node(node_ip, node_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((node_ip, node_port))
            s.sendall(b'get_chain')
            response = s.recv(4096)
            return response.decode()
    except Exception as e:
        print(f"Error getting chain from {node_ip}:{node_port} - {e}")
        return None

def send_signal_to_node(node_ip, node_port, signal):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((node_ip, node_port))
            s.sendall(signal.encode())
            response = s.recv(1024)
            print('response: ', response)
            return response.decode()
    except Exception as e:
        print(f"Error sending signal to {node_ip}:{node_port} - {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: client.py <NODE_IP> <NODE_PORT> <COMMAND>")
        sys.exit(1)

    node_ip = sys.argv[1]
    node_port = int(sys.argv[2])
    command = sys.argv[3]
    if command == 'get_chain':
        chain = get_chain_from_node(node_ip, node_port)
        if chain:
            print(chain)
    elif command == 'add_block':
        response = send_signal_to_node(node_ip, node_port, 'add_block')
        if response:
            print(response)
    else:
        print(f"Unknown command: {command}")
