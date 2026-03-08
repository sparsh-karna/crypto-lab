import socket
import hashlib


def compute_md5(message):
    """Compute MD5 hash of a message"""
    md5_hash = hashlib.md5(message.encode()).hexdigest()
    return md5_hash


def main():
    message = input("Enter message to hash: ")
    
    # Compute MD5 hash
    md5_hash = compute_md5(message)
    
    print(f"\nOriginal message: {message}")
    print(f"MD5 hash: {md5_hash}")
    
    # Send to client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5004))
    server_socket.listen(1)
    print("\nServer started. Waiting for client...")
    
    conn, addr = server_socket.accept()
    print("Client connected.")
    
    # Send original message and hash
    data = f"{message}|{md5_hash}\n"
    conn.sendall(data.encode())
    
    print("Message and hash sent to client")
    
    conn.close()
    server_socket.close()


if __name__ == "__main__":
    main()
