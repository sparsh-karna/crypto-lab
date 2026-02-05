import numpy as np
import math
import socket


def mod_inverse(a, m):
    """Find modular inverse of a under modulo m using extended Euclidean algorithm"""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        return None  # Modular inverse doesn't exist
    return (x % m + m) % m


def mul(p, k):
    """Matrix multiplication with mod 26"""
    result = np.dot(k, p) % 26
    return result


def make_matrix(text, rows, cols):
    """Create matrix from text string"""
    matrix = np.zeros((rows, cols), dtype=int)
    idx = 0
    for i in range(rows):
        for j in range(cols):
            if idx >= len(text):
                matrix[i][j] = (ord('X') - ord('A')) % 26
            else:
                matrix[i][j] = (ord(text[idx]) - ord('A')) % 26
                idx += 1
    return matrix


def encode(result):
    """Convert matrix back to cipher string"""
    cipher = ""
    for row in result:
        for val in row:
            cipher += chr(int(val) + ord('A'))
    return cipher


def main():
    plain_text = input("Enter plaintext: ").strip().upper()
    key = input("Enter key: ").strip().upper()

    n = len(plain_text)
    if n * n != len(key):
        n = math.ceil(math.sqrt(len(key)))

    # Create key matrix (n x n)
    key_matrix = make_matrix(key, n, n)
    print("Key matrix:")
    print(key_matrix)

    # Check if key matrix is invertible mod 26
    det = int(round(np.linalg.det(key_matrix))) % 26
    if mod_inverse(det, 26) is None:
        print("Error: Key matrix is not invertible mod 26")
        print("Please choose a different key where det(key) is coprime with 26")
        return

    # Create plain text matrix (n x cols)
    cols = math.ceil(len(plain_text) / n)
    plain_matrix = make_matrix(plain_text, n, cols)

    # Multiply: key_matrix (n x n) * plain_matrix (n x cols)
    result = mul(plain_matrix, key_matrix)

    cipher = encode(result)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)
    print("Server started. Waiting for client...")

    conn, addr = server_socket.accept()
    print("Client connected.")

    conn.sendall((cipher + "\n").encode())

    print("Encrypted message sent:", cipher)

    conn.close()
    server_socket.close()


if __name__ == "__main__":
    main()
