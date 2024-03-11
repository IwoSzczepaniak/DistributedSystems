import java.util.ArrayList;
import java.util.List;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.ServerSocket;
import java.net.InetAddress;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

public class Server {
    private static int PORT; 
    private static final int BUFFER_SIZE = 1024;
    private static List<ClientHandler> clients = new ArrayList<>();

    private static class TcpServer implements Runnable {
        @Override
        public void run() {
            ServerSocket serverSocket = null;
            try {
                serverSocket = new ServerSocket(PORT);
                System.out.println("TCP Chat Server is running on port " + PORT);

                while (true) {
                    Socket clientSocket = serverSocket.accept();
                    ClientHandler clientHandler = new ClientHandler(clientSocket);
                    clients.add(clientHandler);
                    new Thread(clientHandler).start();
                }
            } catch (Exception e) {
                e.printStackTrace();
            } finally{
                try{
                    if(serverSocket != null){
                        serverSocket.close();
                    }
                } catch (Exception ex){
                    ex.printStackTrace();
                }
            }
        }
    }

    private static class UdpServer implements Runnable {
        @Override
        public void run() {
            DatagramSocket serverSocket = null;
            try {
                serverSocket = new DatagramSocket(PORT);
                System.out.println("UDP Chat Server is running on port " + PORT);
                byte[] receiveBuffer = new byte[BUFFER_SIZE];

                while (true) {
                    DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, BUFFER_SIZE);
                    serverSocket.receive(receivePacket);
                    String message = new String(receivePacket.getData(), 0, receivePacket.getLength());
                    message = "UDP message: " + message;
                    System.out.println(message);
                    broadcastMessage(message, null);
                }
            } catch (Exception e) {
                e.printStackTrace();
            } finally{
                try{
                    if(serverSocket != null){
                        serverSocket.close();
                    }
                } catch (Exception ex){
                    ex.printStackTrace();
                }
            }
                
        }
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Usage: java Server <port>");
            System.exit(1);
        }
        PORT = Integer.valueOf(args[0]);
        new Thread(new TcpServer()).start();
        new Thread(new UdpServer()).start();
    }

    static void broadcastMessage(String message, ClientHandler sender) {
        for (ClientHandler client : clients) {
            if (client != sender) {
                client.sendMessage(message);
            }
        }
    }
}
