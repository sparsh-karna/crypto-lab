import socket


def encode(plain, key):
    """Encode using Vigenere cipher"""
    cipher = ""
    for i in range(len(plain)):
        pi = plain[i]
        ki = key[i % len(key)]
        cipher += chr(((ord(pi) - ord('A') + ord(ki) - ord('A')) % 26) + ord('A'))
    return cipher


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(1)
    print("Server started. Waiting for client...")

    conn, addr = server_socket.accept()
    print("Client connected.")

    plain_text = input("Enter plaintext (uppercase letters only): ").upper()
    key = input("Enter key (uppercase letters only): ").upper()

    cipher = encode(plain_text, key)

    conn.sendall((cipher + "\n").encode())

    print("Ciphertext sent to client:", cipher)

    conn.close()
    server_socket.close()


if __name__ == "__main__":
    main()
