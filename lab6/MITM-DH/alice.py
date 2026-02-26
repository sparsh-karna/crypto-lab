import socket
import random


def power(a, b, p):
    """Compute (a^b) mod p"""
    return pow(a, b, p)


def main():
    # Public DH parameters
    P = 23  # Prime number
    G = 5   # Primitive root
    
    # Alice's private key
    a = random.randint(1, P - 1)
    print(f"Alice's private key: {a}")
    
    # Alice's public key
    A = power(G, a, P)
    print(f"Alice's public key: {A}")
    
    # Connect to Bob (or Eve if MITM is active)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5001))
    
    # Send public key to Bob
    client_socket.sendall(f"{A}\n".encode())
    print(f"Sent public key to Bob: {A}")
    
    # Receive Bob's public key
    B = int(client_socket.recv(1024).decode().strip())
    print(f"Received Bob's public key: {B}")
    
    # Calculate shared secret
    shared_secret = power(B, a, P)
    print(f"Shared secret: {shared_secret}")
    
    # Send encrypted message (simple XOR with shared secret)
    message = "HELLO"
    encrypted = ''.join(chr(ord(c) ^ shared_secret) for c in message)
    client_socket.sendall(f"{encrypted}\n".encode())
    print(f"Sent encrypted message: {repr(encrypted)}")
    
    client_socket.close()


if __name__ == "__main__":
    main()
