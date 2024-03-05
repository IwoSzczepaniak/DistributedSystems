import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.Socket;

public class Client {

    private static void sendViaUDP(String serverHost, int portNumber, String message){
        DatagramSocket socket = null;

        try {
            InetAddress address = InetAddress.getByName(serverHost);
            
            socket = new DatagramSocket();
            byte[] sendBuffer = message.getBytes();

            DatagramPacket sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length, address, portNumber);
            socket.send(sendPacket);

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (socket != null) {
                socket.close();
            }
        }
    }

    public static void main(String[] args) {

        if (args.length != 2) {
            System.err.println("Usage: java Client <username> <port>");
            System.exit(1);
        }

        String serverHost = "localhost"; 
        String username = args[0];
        int port = Integer.valueOf(args[1]);
        Socket socket = null;

        try {
            socket = new Socket(serverHost, port); 
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            out.println(username);

            Thread receivingThread = new Thread(() -> {
                try {
                    String message;
                    while ((message = in.readLine()) != null) {
                        System.out.println(message);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });
            receivingThread.start();

            BufferedReader consoleInput = new BufferedReader(new InputStreamReader(System.in));
            String message;
            while ((message = consoleInput.readLine()) != null) {
                if (message.startsWith("U ")) {
                    sendViaUDP(serverHost, port, message.substring(2));
                } else {
                    out.println(message);
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        } finally{
            try{
                if (socket != null) socket.close();
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }
    }
}

