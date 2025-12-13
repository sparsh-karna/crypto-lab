import java.util.*;

class Server {

    static void makeTable(String k, char[][] kt) {
        int[] hash = new int[26];
        int r = 0;
        int col = 0;
        for (int i = 0; i < k.length(); i++) {
            char c = k.charAt(i);
            if (c < 'A' || c > 'Z')
                continue;
            if (c == 'J')
                c = 'I';
            int ci = c - 'A';
            if (hash[ci] == 0) {
                kt[r][col] = c;
                hash[ci] = 1;
                if (c == 'I') {
                    hash['J' - 'A'] = 1;
                }
            }
            col++;
            if (col == 5) {
                col = 0;
                r++;
            }
        }
        for (char c = 'A'; c <= 'Z'; c++) {
            if (c == 'J')
                continue;
            int ci = c - 'A';
            if (hash[ci] == 0) {
                kt[r][col] = c;
                hash[ci] = 1;
                col++;
                if (col == 5) {
                    col = 0;
                    r++;
                }
            }
        }
    }

    static int[] findPosition(char ch, char[][] kt) {
        if (ch == 'J')
            ch = 'I';
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                if (kt[i][j] == ch) {
                    return new int[] { i, j };
                }
            }
        }
        return null;
    }

    static String encode(String p, char[][] kt) {
        p = p.toUpperCase();
        String prepared = "";
        int i = 0;
        while (i < p.length()) {
            char a = p.charAt(i);
            if (a < 'A' || a > 'Z') {
                i++;
                continue;
            }
            if (a == 'J')
                a = 'I';
            prepared += a;
            i++;
        }
        String digraphs = "";
        i = 0;
        while (i < prepared.length()) {
            char a = prepared.charAt(i);
            digraphs += a;
            if (i == prepared.length() - 1) {
                digraphs += 'X';
                break;
            }
            char b = prepared.charAt(i + 1);
            if (a == b) {
                digraphs += 'X';
            } else {
                digraphs += b;
                i++;
            }
            i++;
        }
        String newCipher = "";
        for (i = 0; i < digraphs.length(); i += 2) {
            char curr = digraphs.charAt(i);
            char nex = digraphs.charAt(i + 1);
            int[] ci = findPosition(curr, kt);
            int[] ni = findPosition(nex, kt);
            if (ci[0] == ni[0]) {
                newCipher += kt[ci[0]][(ci[1] + 1) % 5];
                newCipher += kt[ni[0]][(ni[1] + 1) % 5];
            } else if (ci[1] == ni[1]) {
                newCipher += kt[(ci[0] + 1) % 5][ci[1]];
                newCipher += kt[(ni[0] + 1) % 5][ni[1]];
            } else {
                newCipher += kt[ci[0]][ni[1]];
                newCipher += kt[ni[0]][ci[1]];
            }
        }
        return newCipher;
    }

    public static void main(String args[]) {
        Scanner input = new Scanner(System.in);
        String key = input.nextLine().toUpperCase();
        String plain = input.nextLine();
        char[][] keyTable = new char[5][5];
        makeTable(key, keyTable);
        String cipher = encode(plain, keyTable);
        System.out.println(cipher);
        input.close();
    }
}