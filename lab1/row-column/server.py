import socket
import math
import numpy as np


def swap_col(table, i, j):
    """Swap two columns in the table"""
    table[:, [i, j]] = table[:, [j, i]]


def sort_table(table, key):
    """Sort columns based on key alphabetical order"""
    key_arr = list(key)
    n = len(key)
    for i in range(n):
        for j in range(n - i - 1):
            if key_arr[j] > key_arr[j + 1]:
                swap_col(table, j, j + 1)
                key_arr[j], key_arr[j + 1] = key_arr[j + 1], key_arr[j]


def encode(table, key):
    """Encode by reading columns after sorting"""
    sort_table(table, key)
    cipher = ""
    rows, cols = table.shape
    for c in range(cols):
        for r in range(rows):
            cipher += table[r][c]
    return cipher


def make_table(plain, key):
    """Create the table from plaintext"""
    cols = len(key)
    rows = math.ceil(len(plain) / cols)
    table = np.empty((rows, cols), dtype=str)

    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx < len(plain):
                table[r][c] = plain[idx]
                idx += 1
            else:
                table[r][c] = '_'

    return table


def main():
    plain_text = input("Enter message: ")
    key = input("Enter key: ")

    table = make_table(plain_text, key)
    cipher = encode(table, key)

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
