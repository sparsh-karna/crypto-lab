import java.util.*;
import java.net.*;
import java.io.*;

class Client {

    static String decrypt(char[][] rt, String k) {
        String plain = "";
        int rows = rt.length;
        char[] sortedKey = k.toCharArray();
        Arrays.sort(sortedKey);
        for (char ch : sortedKey) {
            int colIndex = k.indexOf(ch);
            for (int r = 0; r < rows; r++) {
                plain += rt[r][colIndex];
            }
            k = k.substring(0, colIndex) + '_' + k.substring(colIndex + 1);
        }
        return plain.replace("_", "");
    }

    public static void main(String args[]) {
        Scanner input = new Scanner(System.in);
        try {
            Socket socket = new Socket("localhost", 5000);

            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            String cipher = in.readLine();

            System.out.println("Ciphertext received: " + cipher);

            System.out.print("Enter key: ");
            String key = input.nextLine();

            int cols = key.length();
            int rows = (int) Math.ceil((double) cipher.length() / cols);
            char[][] ranktable = new char[rows][cols];

            int idx = 0;
            for (int c = 0; c < cols; c++) {
                for (int r = 0; r < rows; r++) {
                    if (idx < cipher.length()) {
                        ranktable[r][c] = cipher.charAt(idx++);
                    } else {
                        ranktable[r][c] = '_';
                    }
                }
            }

            String plain = decrypt(ranktable, key);
            System.out.println("Decrypted (original) message: " + plain);

            socket.close();
            input.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}