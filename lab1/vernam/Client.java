import java.util.*;
import java.net.*;
import java.io.*;

class Client {
    static String decode(String c, String k) {
        StringBuilder p = new StringBuilder();
        for (int i = 0; i < c.length(); i++) {
            char pc = (char) (((c.charAt(i) - 'A') ^ (k.charAt(i) - 'A')) % 26 + 'A');
            p.append(pc);
        }
        return p.toString();
    }

    public static void main(String args[]) throws Exception {
        Socket s = new Socket("localhost", 1234);
        
        BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
        Scanner sc = new Scanner(System.in);
        
        String ciphertext = in.readLine();
        
        String key = sc.nextLine().toUpperCase();
        
        String plaintext = decode(ciphertext, key);
        
        System.out.println("Ciphertext: " + ciphertext);
        System.out.println("Plaintext: " + plaintext);
        
        s.close();
        sc.close();
    }
}