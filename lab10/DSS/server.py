import socket
import random
import hashlib
import math


def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


def mod_inverse(a, m):
    """Find modular inverse of a under modulo m"""
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return x % m


def compute_generator(p, q):
    """Compute generator g = h^((p-1)/q) mod p"""
    exponent = (p - 1) // q
    for h in range(2, p):
        g = pow(h, exponent, p)
        if g > 1:
            return g
    return None


def hash_message(message):
    """Compute SHA-1 hash as integer"""
    return int(hashlib.sha1(message.encode()).hexdigest(), 16)


def sign_message(message, p, q, g, x):
    """Create DSA signature (r, s)"""
    hash_value = hash_message(message) % q

    while True:
        k = random.randint(1, q - 1)
        if math.gcd(k, q) != 1:
            continue

        r = pow(g, k, p) % q
        if r == 0:
            continue

        k_inv = mod_inverse(k, q)
        s = (k_inv * (hash_value + x * r)) % q
        if s == 0:
            continue

        return r, s, hash_value, k


def main():
    q = int(input("Enter prime number q: "))
    while not is_prime(q):
        q = int(input(f"{q} is not prime. Enter prime number q: "))

    p = int(input("Enter prime number p (p > q and (p-1) % q == 0): "))
    while not (is_prime(p) and p > q and (p - 1) % q == 0):
        p = int(input("Invalid p. Enter prime p where p > q and (p-1) % q == 0: "))

    g = compute_generator(p, q)
    if g is None:
        print("Could not compute generator g for given p and q")
        return

    # Private key x in [1, q-1]
    x = random.randint(1, q - 1)
    # Public key y = g^x mod p
    y = pow(g, x, p)

    print(f"\nGenerator (g): {g}")
    print(f"Private key (x): {x}")
    print(f"Public key (y): {y}")

    message = input("\nEnter message to sign: ")

    r, s, hash_value, k = sign_message(message, p, q, g, x)

    print(f"\nMessage hash (mod q): {hash_value}")
    print(f"Random nonce (k): {k}")
    print(f"Signature: (r={r}, s={s})")

    # Send message, signature, and public parameters to client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5006))
    server_socket.listen(1)
    print("\nServer started. Waiting for client...")

    conn, addr = server_socket.accept()
    print("Client connected.")

    data = f"{message}\n{r}\n{s}\n{p}\n{q}\n{g}\n{y}\n"
    conn.sendall(data.encode())

    print("Message and signature sent to client")

    conn.close()
    server_socket.close()


if __name__ == "__main__":
    main()