import java.io.*;
import java.net.*;
import java.util.*;

class Client {

    static String decrypt(String c, int k) {
        String p = "";
        char[][] rail = new char[k][c.length()];
        boolean dir_down = true;
        int row = 0;
        for (int i = 0; i < c.length(); i++) {
            rail[row][i] = '*';
            if (dir_down) {
                if (row == k - 1) {
                    dir_down = false;
                    row--;
                } else {
                    row++;
                }
            } else {
                if (row == 0) {
                    dir_down = true;
                    row++;
                } else {
                    row--;
                }
            }
        }
        int index = 0;
        for (int i = 0; i < k; i++) {
            for (int j = 0; j < c.length(); j++) {
                if (rail[i][j] == '*') {
                    rail[i][j] = c.charAt(index++);
                }
            }
        }
        dir_down = true;
        row = 0;
        for (int i = 0; i < c.length(); i++) {
            p += rail[row][i];
            if (dir_down) {
                if (row == k - 1) {
                    dir_down = false;
                    row--;
                } else {
                    row++;
                }
            } else {
                if (row == 0) {
                    dir_down = true;
                    row++;
                } else {
                    row--;
                }
            }
        }
        return p;
    }

    public static void main(String args[]) {
        try {
            Socket socket = new Socket("localhost", 5000);

            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            String encrypted = in.readLine();

            System.out.println("Encrypted message received: " + encrypted);

            Scanner input = new Scanner(System.in);

            System.out.print("Enter key: ");
            int n = input.nextInt();

            String decrypted = decrypt(encrypted, n);
            System.out.println("Decrypted (original) message: " + decrypted);

            socket.close();
            input.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
