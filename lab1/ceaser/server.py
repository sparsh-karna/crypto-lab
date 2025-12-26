import socket


def encrypt(s, n):
    new_s = ""
    for c in s:
        if 'a' <= c <= 'z':
            new_s += chr((ord(c) - ord('a') + n) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            new_s += chr((ord(c) - ord('A') + n) % 26 + ord('A'))
        else:
            new_s += c
    return new_s


def main():
    message = input("Enter message: ")
    n = int(input("Enter key: "))

    encrypted = encrypt(message, n)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)
    print("Server started. Waiting for client...")

    conn, addr = server_socket.accept()
    print("Client connected.")

    conn.sendall((encrypted + "\n").encode())

    print("Encrypted message sent:", encrypted)

    conn.close()
    server_socket.close()


if __name__ == "__main__":
    main()
