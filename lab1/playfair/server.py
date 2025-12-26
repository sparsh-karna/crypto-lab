import numpy as np


def make_table(key):
    """Create 5x5 Playfair key table"""
    key_table = np.empty((5, 5), dtype=str)
    used = [False] * 26
    row, col = 0, 0

    for c in key:
        if c < 'A' or c > 'Z':
            continue
        if c == 'J':
            c = 'I'
        ci = ord(c) - ord('A')
        if not used[ci]:
            key_table[row][col] = c
            used[ci] = True
            if c == 'I':
                used[ord('J') - ord('A')] = True
            col += 1
            if col == 5:
                col = 0
                row += 1

    for c in range(ord('A'), ord('Z') + 1):
        ch = chr(c)
        if ch == 'J':
            continue
        ci = c - ord('A')
        if not used[ci]:
            key_table[row][col] = ch
            used[ci] = True
            col += 1
            if col == 5:
                col = 0
                row += 1

    return key_table


def find_position(ch, key_table):
    """Find position of character in key table"""
    if ch == 'J':
        ch = 'I'
    for i in range(5):
        for j in range(5):
            if key_table[i][j] == ch:
                return (i, j)
    return None


def encode(plain, key_table):
    """Encode plaintext using Playfair cipher"""
    plain = plain.upper()

    # Remove non-alphabetic characters and replace J with I
    prepared = ""
    for c in plain:
        if 'A' <= c <= 'Z':
            if c == 'J':
                c = 'I'
            prepared += c

    # Create digraphs
    digraphs = ""
    i = 0
    while i < len(prepared):
        a = prepared[i]
        digraphs += a
        if i == len(prepared) - 1:
            digraphs += 'X'
            break
        b = prepared[i + 1]
        if a == b:
            digraphs += 'X'
        else:
            digraphs += b
            i += 1
        i += 1

    # Encode digraphs
    cipher = ""
    for i in range(0, len(digraphs), 2):
        curr = digraphs[i]
        nex = digraphs[i + 1]
        ci = find_position(curr, key_table)
        ni = find_position(nex, key_table)

        if ci[0] == ni[0]:  # Same row
            cipher += key_table[ci[0]][(ci[1] + 1) % 5]
            cipher += key_table[ni[0]][(ni[1] + 1) % 5]
        elif ci[1] == ni[1]:  # Same column
            cipher += key_table[(ci[0] + 1) % 5][ci[1]]
            cipher += key_table[(ni[0] + 1) % 5][ni[1]]
        else:  # Rectangle
            cipher += key_table[ci[0]][ni[1]]
            cipher += key_table[ni[0]][ci[1]]

    return cipher


def main():
    key = input().strip().upper()
    plain = input().strip()

    key_table = make_table(key)
    cipher = encode(plain, key_table)
    print(cipher)


if __name__ == "__main__":
    main()
