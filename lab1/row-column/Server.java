import java.io.*;
import java.net.*;
import java.util.*;

class Server {

    static void swapCol(char[][] rt, int i, int j) {
        for (int k = 0; k < rt.length; k++) {
            char temp = rt[k][i];
            rt[k][i] = rt[k][j];
            rt[k][j] = temp;
        }
    }

    static void sortTable(char[][] rt, String k) {
        char[] keyArr = k.toCharArray();
        for (int i = 0; i < k.length(); i++) {
            for (int j = 0; j < k.length() - i - 1; j++) {
                if (keyArr[j] > keyArr[j + 1]) {
                    swapCol(rt, j, j + 1);
                    char temp = keyArr[j];
                    keyArr[j] = keyArr[j + 1];
                    keyArr[j + 1] = temp;
                }
            }
        }
    }

    static String encode(char[][] rt, String k) {
        String cipher = "";
        sortTable(rt, k);
        for (int i = 0; i < k.length(); i++) {
            for (int j = 0; j < rt.length; j++) {
                cipher += rt[j][i];
            }
        }
        return cipher;
    }

    static void makeTable(String p, String k, char[][] rt) {
        int idx = 0;
        for (int r = 0; r < rt.length; r++) {
            for (int c = 0; c < rt[0].length; c++) {
                if (idx < p.length()) {
                    rt[r][c] = p.charAt(idx++);
                } else {
                    rt[r][c] = '_';
                }
            }
        }
    }

    public static void main(String args[]) {
        try {
            Scanner input = new Scanner(System.in);

            System.out.print("Enter message: ");
            String plainText = input.nextLine();

            System.out.print("Enter key: ");
            String key = input.nextLine();

            int cols = key.length();
            int rows = (int) Math.ceil((double) plainText.length() / cols);
            char[][] ranktable = new char[rows][cols];
            makeTable(plainText, key, ranktable);
            String cipher = encode(ranktable, key);

            ServerSocket serverSocket = new ServerSocket(5000);
            System.out.println("Server started. Waiting for client...");

            Socket socket = serverSocket.accept();
            System.out.println("Client connected.");

            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

            out.println(cipher);

            System.out.println("Encrypted message sent: " + cipher);

            socket.close();
            serverSocket.close();
            input.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}