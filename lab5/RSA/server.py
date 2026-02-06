import socket
import math


def isPrime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def gcd(a, b):
    if a == 0:
        return b
    return gcd(b % a, a)


def encrypt(M, e, n):
    return int(pow(M, e, n))


def main():
    p = int(input("Enter prime number p: "))
    while not isPrime(p):
        p = int(input(f"{p} is not a prime number\nEnter a prime number p: "))
    
    q = int(input("Enter prime number q: "))
    while not isPrime(q):
        q = int(input(f"{q} is not a prime number\nEnter a prime number q: "))

    n = p * q
    phi = (p - 1) * (q - 1)

    # Find public exponent e
    e = 0
    for i in range(2, phi):
        if gcd(i, phi) == 1:
            e = i
            break

    # Find private exponent d
    d = 0
    for i in range(1, phi + 1):
        if (e * i) % phi == 1:
            d = i
            break

    print(f"\nPublic Key: (e={e}, n={n})")
    print(f"Private Key: (d={d}, n={n})")

    M = input("\nEnter plaintext (string or number): ")
    
    # Check if input is numeric or string
    try:
        # Try to convert to number
        M_num = int(M)
        if M_num >= n:
            print(f"Error: Plaintext value {M_num} is >= n={n}. Please use larger primes.")
            return
        # Encrypt as single number
        C = encrypt(M_num, e, n)
        encrypted_data = f"NUM:{C}"
        print(f"Encrypted message: {C}")
    except ValueError:
        # Check if n is large enough for string encryption
        max_ascii = max(ord(char) for char in M)
        if max_ascii >= n:
            print(f"Error: n={n} is too small for this text (max ASCII: {max_ascii})")
            print(f"Please use larger primes (recommended: p and q both > 127)")
            return
        # Encrypt as string (each character separately)
        encrypted_chars = []
        for char in M:
            ascii_val = ord(char)
            encrypted_val = encrypt(ascii_val, e, n)
            encrypted_chars.append(str(encrypted_val))
        encrypted_data = "STR:" + ",".join(encrypted_chars)
        print(f"Encrypted message: {encrypted_data}")

    # Send encrypted message and keys to client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen(1)
    print("\nServer started. Waiting for client...")

    conn, addr = server_socket.accept()
    print("Client connected.")

    # Send encrypted message, private key d, and n
    message = f"{encrypted_data}|{d}|{n}\n"
    conn.sendall(message.encode())

    print(f"Encrypted message sent")

    conn.close()
    server_socket.close()


if __name__ == "__main__":
    main()
