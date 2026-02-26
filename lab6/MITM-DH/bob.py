import socket
import random


def power(a, b, p):
    """Compute (a^b) mod p"""
    return pow(a, b, p)


def main():
    # Public DH parameters
    P = 23  # Prime number
    G = 5   # Primitive root
    
    # Bob's private key
    b = random.randint(1, P - 1)
    print(f"Bob's private key: {b}")
    
    # Bob's public key
    B = power(G, b, P)
    print(f"Bob's public key: {B}")
    
    # Start server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5002))
    server_socket.listen(1)
    print("Bob waiting on port 5002...\n")
    
    conn, addr = server_socket.accept()
    print("Alice connected")
    
    # Receive Alice's public key
    A = int(conn.recv(1024).decode().strip())
    print(f"Received Alice's public key: {A}")
    
    # Send Bob's public key
    conn.sendall(f"{B}\n".encode())
    print(f"Sent public key to Alice: {B}")
    
    # Calculate shared secret
    shared_secret = power(A, b, P)
    print(f"Shared secret: {shared_secret}")
    
    # Receive encrypted message
    encrypted = conn.recv(1024).decode().strip()
    print(f"Received encrypted message: {repr(encrypted)}")
    
    # Decrypt message
    decrypted = ''.join(chr(ord(c) ^ shared_secret) for c in encrypted)
    print(f"Decrypted message: {decrypted}")
    
    conn.close()
    server_socket.close()


if __name__ == "__main__":
    main()
