import java.io.*;
import java.net.*;
import java.util.*;

public class Client {

    static String decrypt(String s, int n) {
        String new_s = "";
        for (char c : s.toCharArray()) {
            if (c >= 'a' && c <= 'z') {
                new_s += (char) ((c - 'a' - n + 26) % 26 + 'a');
            } else if (c >= 'A' && c <= 'Z') {
                new_s += (char) ((c - 'A' - n + 26) % 26 + 'A');
            } else {
                new_s += c;
            }
        }
        return new_s;
    }

    public static void main(String[] args) {
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
