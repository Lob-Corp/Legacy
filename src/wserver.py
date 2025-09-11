import socket
import threading
import sys
from typing import Callable, List, Tuple, Optional


class ServerConfig:
    def __init__(self, port: int = 8080, address: str = "127.0.0.1", cgi: bool = False, no_fork: bool = False):
        self.port = port
        self.address = address
        self.cgi = cgi
        self.no_fork = no_fork
        self.stop_server: bool = False
        self.sock_in: Optional[int] = None
        self.sock_out: Optional[int] = None


class WServer:
    def __init__(self, handler: Callable[[List[str], str], str], config: Optional[ServerConfig] = None):
        self.handler = handler
        self.config = config or ServerConfig()
        self._sock: Optional[socket.socket] = None
        self._running = False
        self._threads: List[threading.Thread] = []

    def start(self, use_network: bool = False):
        self.config.sock_in = self.config.port
        self.config.stop_server = False
        self._running = True

        if not use_network:
            # Simulated mode for tests
            return f"Server started on {self.config.address}:{self.config.port} (simulated)"

        # Real network mode
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.config.address, self.config.port))
        self._sock.listen(5)

        while not self.config.stop_server:
            try:
                client_sock, addr = self._sock.accept()
            except OSError:
                break

            if self.config.no_fork:
                self._handle_client(client_sock, addr)
            else:
                t = threading.Thread(target=self._handle_client, args=(client_sock, addr), daemon=True)
                t.start()
                self._threads.append(t)

        if self._sock:
            self._sock.close()
            self._sock = None

    def stop(self):
        self.config.stop_server = True
        self._running = False
        if self._sock:
            try:
                self._sock.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            self._sock.close()

    def _handle_client(self, client_sock: socket.socket, addr):
        try:
            request_data = client_sock.recv(4096).decode("utf-8", errors="ignore")
            if not request_data:
                client_sock.close()
                return

            headers, body = get_request_and_content(request_data)
            response = self.handler(headers, body)
            http(client_sock, 200, response)
        except Exception as e:
            http(client_sock, 500, f"Internal Server Error: {e}")
        finally:
            client_sock.close()


def run_server(handler: Callable[[List[str], str], str], port: int = 8080, address: str = "127.0.0.1", use_network: bool = False, cgi: bool = False, no_fork: bool = False):
    config = ServerConfig(port=port, address=address, cgi=cgi, no_fork=no_fork)
    server = WServer(handler, config=config)
    return server.start(use_network=use_network)


# --- HTTP helpers ---

def get_request_and_content(request: str) -> Tuple[List[str], str]:
    """
    Parse raw HTTP request string and return (headers, body).
    For test compatibility: also works if input is an iterable of chars.
    """
    if not isinstance(request, str):
        request = "".join(request)
    parts = request.split("\r\n\r\n", 1)
    headers = parts[0].split("\r\n") if parts else []
    body = parts[1] if len(parts) > 1 else ""
    return headers, body


def print_string(s: str):
    sys.stdout.write(s)


def header(key: str, value: str) -> str:
    return f"{key}: {value}\r\n"


def wflush():
    sys.stdout.flush()


def http(sock_or_fd, status_code: int, body: str):
    response = (
        f"HTTP/1.1 {status_code} {'OK' if status_code == 200 else 'Error'}\r\n"
        f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        f"Content-Type: text/plain; charset=utf-8\r\n"
        "\r\n"
        f"{body}"
    )
    if isinstance(sock_or_fd, socket.socket):
        sock_or_fd.sendall(response.encode("utf-8"))
    else:
        sys.stdout.write(response)


def http_redirect_temporarily(sock_or_fd, location: str):
    response = (
        "HTTP/1.1 302 Found\r\n"
        f"Location: {location}\r\n"
        "\r\n"
    )
    if isinstance(sock_or_fd, socket.socket):
        sock_or_fd.sendall(response.encode("utf-8"))
    else:
        sys.stdout.write(response)


def close_connection(sock: socket.socket):
    try:
        sock.shutdown(socket.SHUT_RDWR)
    except Exception:
        pass
    sock.close()


# --- Legacy placeholders (not used in Python but kept for parity with .mli) ---

def printf(fmt: str, *args):
    sys.stdout.write(fmt % args)


def wsocket():
    raise NotImplementedError("wsocket is not applicable in Python.")


def woc():
    raise NotImplementedError("woc is not applicable in Python.")
