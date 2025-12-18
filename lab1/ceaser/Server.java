import java.io.*;
import java.net.*;
import java.util.*;

public class Server {

    static String encrypt(String s, int n) {
        String new_s = "";
        for (char c : s.toCharArray()) {
            if (c >= 'a' && c <= 'z') {
                new_s += (char) ((c - 'a' + n) % 26 + 'a');
            } else if (c >= 'A' && c <= 'Z') {
                new_s += (char) ((c - 'A' + n) % 26 + 'A');
            } else {
                new_s += c;
            }
        }
        return new_s;
    }

    public static void main(String[] args) {
        try {
            Scanner input = new Scanner(System.in);

            System.out.print("Enter message: ");
            String message = input.nextLine();

            System.out.print("Enter key: ");
            int n = input.nextInt();

            String encrypted = encrypt(message, n);

            ServerSocket serverSocket = new ServerSocket(5000);
            System.out.println("Server started. Waiting for client...");

            Socket socket = serverSocket.accept();
            System.out.println("Client connected.");

            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

            out.println(encrypted);

            System.out.println("Encrypted message sent: " + encrypted);

            socket.close();
            serverSocket.close();
            input.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
