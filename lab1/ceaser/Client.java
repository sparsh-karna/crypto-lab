import java.io.*;
import java.net.*;
import java.util.*;

public class Client {

    static String encrypt(String s, int n){
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

            Socket socket = new Socket("localhost", 5000);

            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

            out.println(encrypted);   
            out.println(n);          

            System.out.println("Encrypted message sent: " + encrypted);

            socket.close();

        } 
        catch (Exception e) {
            e.printStackTrace();
        }
    }
}
