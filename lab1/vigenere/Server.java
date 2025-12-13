import java.util.*;
import java.net.*;
import java.io.*;

class Server {

    static String encode(String p, String k) {
        String c = "";
        for (int i = 0; i < p.length(); i++) {
            char pi = p.charAt(i);
            char ki = k.charAt(i % k.length());
            c += (char)(((pi - 'A' + ki - 'A') % 26) + 'A');
        }
        return c;
    }

    public static void main(String args[]) throws Exception {
        ServerSocket ss = new ServerSocket(9999);
        System.out.println("Server started. Waiting for client...");
        Socket s = ss.accept();
        System.out.println("Client connected.");

        Scanner input = new Scanner(System.in);

        System.out.print("Enter plaintext (uppercase letters only): ");
        String plainText = input.nextLine().toUpperCase();

        System.out.print("Enter key (uppercase letters only): ");
        String key = input.nextLine().toUpperCase();

        String cipher = encode(plainText, key);

        // Send ciphertext to client
        PrintWriter out = new PrintWriter(s.getOutputStream(), true);
        out.println(cipher);

        System.out.println("Ciphertext sent to client: " + cipher);

        out.close();
        s.close();
        ss.close();
        input.close();
    }
}