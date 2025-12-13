import java.util.*;
import java.net.*;
import java.io.*;

class Server {
    static String encode(String p, String k) {
        StringBuilder c = new StringBuilder();
        for (int i = 0; i < p.length(); i++) {
            char pc = (char) (((p.charAt(i) - 'A') ^ (k.charAt(i) - 'A')) % 26 + 'A');
            c.append(pc);
        }
        return c.toString();
    }

    public static void main(String args[]) throws Exception {
        ServerSocket ss = new ServerSocket(1234);
        Socket s = ss.accept();
        Scanner sc = new Scanner(System.in);
        
        String p = sc.nextLine().toUpperCase();
        
        String k = sc.nextLine().toUpperCase();
        
        String ciphertext = encode(p, k);
        
        DataOutputStream out = new DataOutputStream(s.getOutputStream());
        out.writeBytes(ciphertext + "\n");
        
        s.close();
        ss.close();
        sc.close();
    }
}