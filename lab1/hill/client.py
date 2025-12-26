import numpy as np
import math


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


def matrix_mod_inverse(matrix, mod):
    """Find modular inverse of a matrix"""
    det = int(round(np.linalg.det(matrix))) % mod
    det_inv = mod_inverse(det, mod)
    if det_inv is None:
        return None

    # Calculate adjugate matrix
    n = matrix.shape[0]
    adjugate = np.zeros((n, n), dtype=int)

    for i in range(n):
        for j in range(n):
            minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
            cofactor = ((-1) ** (i + j)) * int(round(np.linalg.det(minor)))
            adjugate[j][i] = cofactor

    inverse = (det_inv * adjugate) % mod
    return inverse


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


def decode(result):
    """Convert matrix back to plain text string"""
    plain = ""
    for row in result:
        for val in row:
            plain += chr(int(val) + ord('A'))
    return plain


def main():
    cipher = input().strip()
    key = input().strip()

    n = len(cipher)
    if n * n != len(key):
        n = math.ceil(math.sqrt(len(key)))

    # Create key matrix (n x n)
    key_matrix = make_matrix(key, n, n)

    # Find inverse of key matrix
    key_inverse = matrix_mod_inverse(key_matrix, 26)

    if key_inverse is None:
        print("Key matrix is not invertible mod 26")
        return

    # Create cipher matrix (n x cols)
    cols = math.ceil(len(cipher) / n)
    cipher_matrix = make_matrix(cipher, n, cols)

    # Multiply: key_inverse (n x n) * cipher_matrix (n x cols)
    result = np.dot(key_inverse, cipher_matrix) % 26

    plain = decode(result)
    print(plain)


if __name__ == "__main__":
    main()
