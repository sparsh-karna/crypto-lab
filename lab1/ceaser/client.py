import socket


def decrypt(s, n):
    new_s = ""
    for c in s:
        if 'a' <= c <= 'z':
            new_s += chr((ord(c) - ord('a') - n + 26) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            new_s += chr((ord(c) - ord('A') - n + 26) % 26 + ord('A'))
        else:
            new_s += c
    return new_s


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
