import socket
import hashlib


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


def hash_message(message):
    """Compute SHA-1 hash as integer"""
    return int(hashlib.sha1(message.encode()).hexdigest(), 16)


def verify_signature(message, r, s, p, q, g, y):
    """Verify DSA signature"""
    if not (0 < r < q and 0 < s < q):
        return False, None, None

    hash_value = hash_message(message) % q
    w = mod_inverse(s, q)

    u1 = (hash_value * w) % q
    u2 = (r * w) % q

    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
    return v == r, hash_value, v


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5006))

    # Receive message, signature, and public parameters
    data = client_socket.recv(4096).decode().strip().split('\n')

    if len(data) < 7:
        print("Invalid data received from server")
        client_socket.close()
        return

    message = data[0]
    r = int(data[1])
    s = int(data[2])
    p = int(data[3])
    q = int(data[4])
    g = int(data[5])
    y = int(data[6])

    print(f"Received message: {message}")
    print(f"Received signature: (r={r}, s={s})")
    print(f"Public parameters: p={p}, q={q}, g={g}, y={y}")

    # Verify signature
    is_valid, hash_value, v = verify_signature(message, r, s, p, q, g, y)

    if hash_value is not None:
        print(f"Computed hash (mod q): {hash_value}")
        print(f"Computed verifier value (v): {v}")

    if is_valid:
        print("\n✓ Signature verification successful! Message is authentic.")
    else:
        print("\n✗ Signature verification failed! Message is not authentic.")

    client_socket.close()


if __name__ == "__main__":
    main()