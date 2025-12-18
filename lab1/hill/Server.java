import java.util.*;
import java.io.*;
import java.net.*;

class Server{

    static int[] mul(char[] key, int[][] km){
        int[] ki = new int[key.length];
        for(int i = 0; i < key.length; i++){
            ki[i] = (key[i] - 'A')  % 26;
        }
        int[] res = new int[key.length];
        for(int i = 0; i < key.length; i++){
            int r = 0;
            for(int j = 0; j < key.length; j++){
                r += km[i][j] * key[j];
            }
            r = r % 26;
            res[i] = r;
        }
        return res;
    }

    static void makeMatrix(String k, int[][] kM){
        int idx = 0;
        for(int i = 0; i < kM.lenght; i++){
            for(int j = 0; j < kM[0].lenght; j++){
                kM[i][j] = k.charAt(idx++) - 'A';
            }
        }
    }

    static String encode(){
        String cipher = "";
        for(int i: r){
            cipher += (char)(i + 'A');
        }
        return cipher;
    }

    public static void main(String args[]){
        Scanner input = new Scanner(System.in);
        String plainText = input.nextLine();
        String key = input.nextLine();
        int n = plainText.length();
        int[][] keyMatrix = new int[n][n];
        makeMatrix(key, keyMatrix);
        for(int i: res){
            System.out.println(i);
        }
        String cipher = encode(keyMatrix, plainText);
        System.out.println(cipher);
    }
}