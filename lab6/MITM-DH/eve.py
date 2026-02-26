import socket
import threading
import random


def power(a, b, p):
    """Compute (a^b) mod p"""
    return pow(a, b, p)


P = 23  # Public parameters
G = 5

# Eve's private keys for both connections
e1 = random.randint(1, P - 1)  # For Alice
e2 = random.randint(1, P - 1)  # For Bob

print(f"Eve's private key for Alice: {e1}")
print(f"Eve's private key for Bob: {e2}")


def handle_alice():
    """Impersonate Bob to Alice"""
    # Accept connection from Alice first
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen(1)
    print("\nEve waiting for Alice on port 5001...\n")
    
    alice_conn, _ = server_socket.accept()
    print("Alice connected to Eve")
    
    # Now connect to Bob
    bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bob_socket.connect(('localhost', 5002))
    print("Eve connected to Bob")
    
    # Receive Alice's public key
    A = int(alice_conn.recv(1024).decode().strip())
    print(f"[Eve] Received Alice's public key: {A}")
    
    # Send fake public key to Bob (pretending to be Alice)
    E2 = power(G, e2, P)
    bob_socket.sendall(f"{E2}\n".encode())
    print(f"[Eve] Sent fake public key to Bob: {E2}")
    
    # Receive Bob's public key
    B = int(bob_socket.recv(1024).decode().strip())
    print(f"[Eve] Received Bob's public key: {B}")
    
    # Send fake public key to Alice (pretending to be Bob)
    E1 = power(G, e1, P)
    alice_conn.sendall(f"{E1}\n".encode())
    print(f"[Eve] Sent fake public key to Alice: {E1}")
    
    # Calculate shared secrets
    secret_alice = power(A, e1, P)
    secret_bob = power(B, e2, P)
    print(f"[Eve] Shared secret with Alice: {secret_alice}")
    print(f"[Eve] Shared secret with Bob: {secret_bob}")
    
    # Intercept Alice's encrypted message
    encrypted_from_alice = alice_conn.recv(1024).decode().strip()
    print(f"\n[Eve] Intercepted from Alice: {repr(encrypted_from_alice)}")
    
    # Decrypt Alice's message
    decrypted = ''.join(chr(ord(c) ^ secret_alice) for c in encrypted_from_alice)
    print(f"[Eve] Decrypted Alice's message: {decrypted}")
    
    # Re-encrypt for Bob
    reencrypted = ''.join(chr(ord(c) ^ secret_bob) for c in decrypted)
    bob_socket.sendall(f"{reencrypted}\n".encode())
    print(f"[Eve] Re-encrypted and sent to Bob: {repr(reencrypted)}")
    
    alice_conn.close()
    bob_socket.close()
    server_socket.close()


if __name__ == "__main__":
    print("=== Man-in-the-Middle Attack ===")
    print("Eve will intercept communication between Alice and Bob\n")
    handle_alice()
