import socket
import numpy as np


def decrypt(cipher, key):
    """Decrypt using rail fence cipher"""
    rail = np.zeros((key, len(cipher)), dtype=str)
    rail[:] = ''

    # Mark the positions
    dir_down = True
    row = 0
    for i in range(len(cipher)):
        rail[row][i] = '*'
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

    # Fill the cipher characters
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*':
                rail[i][j] = cipher[index]
                index += 1

    # Read in zig-zag pattern
    plain = ""
    dir_down = True
    row = 0
    for i in range(len(cipher)):
        plain += rail[row][i]
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

    return plain


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    encrypted = client_socket.recv(1024).decode().strip()

    print("Encrypted message received:", encrypted)

    n = int(input("Enter key: "))

    decrypted = decrypt(encrypted, n)
    print("Decrypted (original) message:", decrypted)

    client_socket.close()


if __name__ == "__main__":
    main()
