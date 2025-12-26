import socket
import math
import numpy as np


def decrypt(table, key):
    """Decrypt by reversing the column sort"""
    plain = ""
    rows = table.shape[0]
    sorted_key = sorted(key)

    key_list = list(key)
    for ch in sorted_key:
        col_index = key_list.index(ch)
        for r in range(rows):
            plain += table[r][col_index]
        key_list[col_index] = '_'  # Mark as used

    return plain.replace("_", "")


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    cipher = client_socket.recv(1024).decode().strip()

    print("Ciphertext received:", cipher)

    key = input("Enter key: ")

    cols = len(key)
    rows = math.ceil(len(cipher) / cols)
    table = np.empty((rows, cols), dtype=str)

    idx = 0
    for c in range(cols):
        for r in range(rows):
            if idx < len(cipher):
                table[r][c] = cipher[idx]
                idx += 1
            else:
                table[r][c] = '_'

    plain = decrypt(table, key)
    print("Decrypted (original) message:", plain)

    client_socket.close()


if __name__ == "__main__":
    main()
