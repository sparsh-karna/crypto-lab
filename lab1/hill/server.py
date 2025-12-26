import numpy as np
import math


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
    plain_text = input().strip()
    key = input().strip()

    n = len(plain_text)
    if n * n != len(key):
        n = math.ceil(math.sqrt(len(key)))

    # Create key matrix (n x n)
    key_matrix = make_matrix(key, n, n)

    # Create plain text matrix (n x cols)
    cols = math.ceil(len(plain_text) / n)
    plain_matrix = make_matrix(plain_text, n, cols)

    # Multiply: key_matrix (n x n) * plain_matrix (n x cols)
    result = mul(plain_matrix, key_matrix)

    # Print intermediate results
    for row in result:
        for val in row:
            print(int(val), end="")
        print()

    cipher = encode(result)
    print(cipher)


if __name__ == "__main__":
    main()
