import java.io.*;
import java.net.*;
import java.util.*;

class Server {

    static String encrypt(String p, int k) {
        String c = "";
        char[][] rail = new char[k][p.length()];
        boolean dir_down = true;
        int row = 0;
        for (int i = 0; i < p.length(); i++) {
            rail[row][i] = p.charAt(i);
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
        for (int i = 0; i < k; i++) {
            for (int j = 0; j < p.length(); j++) {
                if (rail[i][j] != 0) {
                    c += rail[i][j];
                }
            }
        }
        return c;
    }

    public static void main(String args[]) {
        try {
            Scanner input = new Scanner(System.in);

            System.out.print("Enter message: ");
            String plainText = input.nextLine();

            System.out.print("Enter key: ");
            int key = input.nextInt();

            String cipher = encrypt(plainText, key);

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
