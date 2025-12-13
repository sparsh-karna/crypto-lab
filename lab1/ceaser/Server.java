import java.io.*;
import java.net.*;
import java.util.*;

public class Server {

    static String decrypt(String s, int n){
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
            ServerSocket serverSocket = new ServerSocket(5000);
            System.out.println("Server started. Waiting for message...");

            Socket socket = serverSocket.accept();
            System.out.println("Client connected.");

            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            String encrypted = in.readLine();      
            int key = Integer.parseInt(in.readLine());   

            System.out.println("Encrypted message received: " + encrypted);

            String decrypted = decrypt(encrypted, key);
            System.out.println("Decrypted (original) message: " + decrypted);

            socket.close();
            serverSocket.close();
        } 
        catch (Exception e) {
            e.printStackTrace();
        }
    }
}
