import socket


def power(a, b, p):
    """Compute (a^b) mod p efficiently"""
    return pow(a, b, p)


def mod_inverse(a, p):
    """Find modular inverse of a under modulo p using Fermat's little theorem"""
    return power(a, p - 2, p)


def decrypt(c1, c2, x, p):
    """Decrypt Elgamal ciphertext"""
    # m = c2 * (c1^x)^-1 mod p
    s = power(c1, x, p)
    s_inv = mod_inverse(s, p)
    m = (c2 * s_inv) % p
    return m


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5003))
    
    # Receive ciphertext and keys
    data = client_socket.recv(1024).decode().strip()
    c1, c2, x, p = map(int, data.split(','))
    
    print(f"Received ciphertext: (c1={c1}, c2={c2})")
    print(f"Private key (x): {x}")
    print(f"Prime (p): {p}")
    
    # Decrypt
    m = decrypt(c1, c2, x, p)
    
    print(f"\nDecrypted (original) message: {m}")
    
    client_socket.close()


if __name__ == "__main__":
    main()
