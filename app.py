from node_server import start_server, blockchain, threading

if __name__ == "__main__":
    # For this example, you can manually add other peer IPs
    # Start the P2P server
    server_thread = threading.Thread(target=start_server, args=(blockchain,))
    server_thread.start()
    # You can now sync chains or add blocks by connecting to this server using a socket connection.
    # This example is very basic. In a real-world scenario, you'd want to add more error checking, validation, and functionality.
