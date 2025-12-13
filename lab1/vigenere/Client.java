import java.util.*;
import java.net.*;
import java.io.*;

class Client {
    static String decode(String c, String k) {
        String p = "";
        for (int i = 0; i < c.length(); i++) {
            char ci = c.charAt(i);
            char ki = k.charAt(i % k.length());
            p += (char)(((ci - 'A' - (ki - 'A') + 26) % 26) + 'A');
        }
        return p;
    }

    public static void main(String args[]) throws Exception {
        Socket s = new Socket("localhost", 9999);
        System.out.println("Connected to server.");

        // Receive ciphertext from server
        BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
        String cipher = in.readLine();

        System.out.println("Received ciphertext: " + cipher);

        // Ask user for key
        Scanner input = new Scanner(System.in);
        System.out.print("Enter the key to decipher: ");
        String key = input.nextLine().toUpperCase();

        // Decipher and display plaintext
        String plainText = decode(cipher, key);
        System.out.println("Deciphered plaintext: " + plainText);

        in.close();
        s.close();
        input.close();
    }
}