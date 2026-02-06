import socket


def decrypt(C, d, n):
    """Decrypt ciphertext using RSA private key"""
    return int(pow(C, d, n))


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5001))

    # Receive encrypted message, private key d, and n
    data = client_socket.recv(1024).decode().strip()
    parts = data.split('|')
    encrypted_data = parts[0]
    d = int(parts[1])
    n = int(parts[2])

    print(f"Encrypted message received: {encrypted_data}")
    print(f"Private key (d={d}, n={n})")

    # Check if encrypted data is string or number
    if encrypted_data.startswith("NUM:"):
        # Decrypt as number
        C = int(encrypted_data[4:])
        M = decrypt(C, d, n)
        print(f"Decrypted (original) message: {M}")
    elif encrypted_data.startswith("STR:"):
        # Decrypt as string
        encrypted_chars = encrypted_data[4:].split(',')
        decrypted_chars = []
        for enc_val in encrypted_chars:
            ascii_val = decrypt(int(enc_val), d, n)
            decrypted_chars.append(chr(ascii_val))
        M = ''.join(decrypted_chars)
        print(f"Decrypted (original) message: {M}")

    client_socket.close()


if __name__ == "__main__":
    main()
