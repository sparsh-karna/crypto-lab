import socket
import numpy as np


def encrypt(plain, key):
    """Encrypt using rail fence cipher"""
    rail = np.zeros((key, len(plain)), dtype=str)
    rail[:] = ''

    dir_down = True
    row = 0

    for i, char in enumerate(plain):
        rail[row][i] = char
        if dir_down:
            if row == key - 1:
                dir_down = False
                row -= 1
            else:
                row += 1
        else:
            if row == 0:
                dir_down = True
                row += 1
            else:
                row -= 1

    cipher = ""
    for i in range(key):
        for j in range(len(plain)):
            if rail[i][j] != '':
                cipher += rail[i][j]

    return cipher


def main():
    plain_text = input("Enter message: ")
    key = int(input("Enter key: "))

    cipher = encrypt(plain_text, key)

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
