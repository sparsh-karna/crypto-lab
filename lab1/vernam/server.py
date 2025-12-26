import socket


def encode(plain, key):
    """Encode using Vernam cipher (XOR)"""
    cipher = ""
    for i in range(len(plain)):
        pc = chr(((ord(plain[i]) - ord('A')) ^ (ord(key[i]) - ord('A'))) % 26 + ord('A'))
        cipher += pc
    return cipher


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 1234))
    server_socket.listen(1)

    conn, addr = server_socket.accept()

    plain = input().strip().upper()
    key = input().strip().upper()

    ciphertext = encode(plain, key)

    conn.sendall((ciphertext + "\n").encode())

    conn.close()
    server_socket.close()


if __name__ == "__main__":
    main()
