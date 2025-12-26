import socket


def decode(cipher, key):
    """Decode using Vernam cipher (XOR)"""
    plain = ""
    for i in range(len(cipher)):
        pc = chr(((ord(cipher[i]) - ord('A')) ^ (ord(key[i]) - ord('A'))) % 26 + ord('A'))
        plain += pc
    return plain


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 1234))

    ciphertext = client_socket.recv(1024).decode().strip()

    key = input().strip().upper()

    plaintext = decode(ciphertext, key)

    print("Ciphertext:", ciphertext)
    print("Plaintext:", plaintext)

    client_socket.close()


if __name__ == "__main__":
    main()
