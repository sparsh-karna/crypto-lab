import socket
import math
import numpy as np


def decrypt(cipher, key):
    """Decrypt by reversing the column sort"""
    cols = len(key)
    rows = math.ceil(len(cipher) / cols)
    
    # Create table to hold sorted columns
    table = np.empty((rows, cols), dtype=str)
    
    # Get the sorted key indices
    key_with_indices = [(char, idx) for idx, char in enumerate(key)]
    sorted_key = sorted(key_with_indices)
    
    # Fill the table column by column from ciphertext (in sorted key order)
    idx = 0
    for _, original_col in sorted_key:
        for r in range(rows):
            if idx < len(cipher):
                table[r][original_col] = cipher[idx]
                idx += 1
            else:
                table[r][original_col] = '_'
    
    # Read row by row to get plaintext
    plain = ""
    for r in range(rows):
        for c in range(cols):
            plain += table[r][c]
    
    return plain.replace("_", "")


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    cipher = client_socket.recv(1024).decode().strip()

    print("Ciphertext received:", cipher)

    key = input("Enter key: ")

    plain = decrypt(cipher, key)
    print("Decrypted (original) message:", plain)

    client_socket.close()


if __name__ == "__main__":
    main()
