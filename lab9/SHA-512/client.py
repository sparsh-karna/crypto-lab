import socket
import hashlib


def compute_sha512(message):
    """Compute SHA-512 hash of a message"""
    sha512_hash = hashlib.sha512(message.encode()).hexdigest()
    return sha512_hash


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5005))

    # Receive hash
    received_hash = client_socket.recv(4096).decode().strip()

    print(f"Received SHA-512 hash: {received_hash}")

    message = input("Enter original message to verify: ")

    # Verify hash for the entered message
    computed_hash = compute_sha512(message)
    print(f"Computed SHA-512 hash: {computed_hash}")

    if received_hash == computed_hash:
        print("\nDecrypted (original) message:", message)
    else:
        print("\nVerification failed! Entered message does not match the hash.")

    client_socket.close()


if __name__ == "__main__":
    main()
