import socket
import random


def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def power(a, b, p):
    """Compute (a^b) mod p efficiently"""
    return pow(a, b, p)


def mod_inverse(a, p):
    """Find modular inverse of a under modulo p using Fermat's little theorem"""
    return power(a, p - 2, p)


def main():
    # Key generation
    p = int(input("Enter a large prime number p: "))
    while not is_prime(p):
        p = int(input(f"{p} is not prime. Enter a prime number p: "))
    
    g = int(input(f"Enter generator g (1 < g < {p}): "))
    
    # Private key
    x = random.randint(2, p - 2)
    print(f"\nPrivate key (x): {x}")
    
    # Public key
    y = power(g, x, p)
    print(f"Public key (y): {y}")
    print(f"Public parameters: p={p}, g={g}")
    
    # Get message
    message = input("\nEnter message (as number): ")
    m = int(message)
    
    if m >= p:
        print(f"Error: Message {m} must be less than p={p}")
        return
    
    # Encryption
    k = random.randint(2, p - 2)  # Random ephemeral key
    print(f"Random key (k): {k}")
    
    c1 = power(g, k, p)
    c2 = (m * power(y, k, p)) % p
    
    print(f"\nCiphertext: (c1={c1}, c2={c2})")
    
    # Send to client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5003))
    server_socket.listen(1)
    print("\nServer started. Waiting for client...")
    
    conn, addr = server_socket.accept()
    print("Client connected.")
    
    # Send ciphertext and keys
    data = f"{c1},{c2},{x},{p}\n"
    conn.sendall(data.encode())
    
    print(f"Encrypted message sent")
    
    conn.close()
    server_socket.close()


if __name__ == "__main__":
    main()
