import socket


def decode(cipher, key):
    """Decode using Vigenere cipher"""
    plain = ""
    for i in range(len(cipher)):
        ci = cipher[i]
        ki = key[i % len(key)]
        plain += chr(((ord(ci) - ord('A') - (ord(ki) - ord('A')) + 26) % 26) + ord('A'))
    return plain


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9999))
    print("Connected to server.")

    cipher = client_socket.recv(1024).decode().strip()

    print("Received ciphertext:", cipher)

    key = input("Enter the key to decipher: ").upper()

    plain_text = decode(cipher, key)
    print("Deciphered plaintext:", plain_text)

    client_socket.close()


if __name__ == "__main__":
    main()
