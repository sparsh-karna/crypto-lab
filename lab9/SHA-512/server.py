import socket
import hashlib


def compute_sha512(message):
    """Compute SHA-512 hash of a message"""
    sha512_hash = hashlib.sha512(message.encode()).hexdigest()
    return sha512_hash


def main():
    message = input("Enter message to hash: ")

    # Compute SHA-512 hash
    sha512_hash = compute_sha512(message)

    print(f"\nOriginal message: {message}")
    print(f"SHA-512 hash: {sha512_hash}")

    # Send to client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5005))
    server_socket.listen(1)
    print("\nServer started. Waiting for client...")

    conn, addr = server_socket.accept()
    print("Client connected.")

    # Send hash to client
    data = f"{sha512_hash}\n"
    conn.sendall(data.encode())

    print("Hash sent to client")

    conn.close()
    server_socket.close()


if __name__ == "__main__":
    main()
