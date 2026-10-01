import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.rmi.server.RMISocketFactory;

/** TLC 2.19 exports its local FPSet through RMI even without distributed mode.
 * Provide a NON-NETWORKING endpoint: no bind, no connect, no remote calls.
 * The model checker and original tla2tools.jar are unchanged.
 * Do not use this launcher for distributed TLC.
 */
public final class LocalTLC {
    private static final class NoNetworkServer extends ServerSocket {
        private boolean stopped;
        NoNetworkServer() throws IOException { super(); }
        @Override public int getLocalPort() { return 1; }
        @Override public synchronized Socket accept() throws IOException {
            while (!stopped) {
                try { wait(); }
                catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    throw new SocketException("Local-only TLC endpoint interrupted");
                }
            }
            throw new SocketException("Local-only TLC endpoint closed");
        }
        @Override public synchronized void close() throws IOException {
            stopped = true;
            notifyAll();
            super.close();
        }
    }
    public static void main(String[] args) throws Exception {
        RMISocketFactory.setSocketFactory(new RMISocketFactory() {
            @Override public ServerSocket createServerSocket(int port) throws IOException {
                return new NoNetworkServer();
            }
            @Override public Socket createSocket(String host, int port) throws IOException {
                throw new SocketException("Networking is disabled in local TLC");
            }
        });
        tlc2.TLC.main(args);
    }
}
