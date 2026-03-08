import socket
import hashlib


def compute_md5(message):
    """Compute MD5 hash of a message"""
    md5_hash = hashlib.md5(message.encode()).hexdigest()
    return md5_hash


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5004))
    
    # Receive message and hash
    data = client_socket.recv(1024).decode().strip()
    message, received_hash = data.split('|')
    
    print(f"Received message: {message}")
    print(f"Received MD5 hash: {received_hash}")
    
    # Verify hash
    computed_hash = compute_md5(message)
    print(f"Computed MD5 hash: {computed_hash}")
    
    if received_hash == computed_hash:
        print("\n✓ Hash verification successful! Message integrity confirmed.")
    else:
        print("\n✗ Hash verification failed! Message may be corrupted.")
    
    client_socket.close()


if __name__ == "__main__":
    main()
