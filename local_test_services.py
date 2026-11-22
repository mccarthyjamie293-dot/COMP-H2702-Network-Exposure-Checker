import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"

class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"COMP H2702 local HTTP test service\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, format, *args):
        return

def run_http():
    server = HTTPServer((HOST, 18080), DemoHandler)
    print("[OPEN] HTTP test service on 127.0.0.1:18080")
    server.serve_forever()

def tcp_server(port, banner):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, port))
        s.listen(5)
        print(f"[OPEN] TCP test service on 127.0.0.1:{port}")
        while True:
            conn, _ = s.accept()
            with conn:
                conn.sendall(banner)

def main():
    services = [
        threading.Thread(target=run_http, daemon=True),
        threading.Thread(target=tcp_server, args=(19090, b"COMP H2702 Banner Service v1.0\r\n"), daemon=True),
        threading.Thread(target=tcp_server, args=(20001, b"COMP H2702 Generic TCP Service\r\n"), daemon=True),
    ]
    for t in services:
        t.start()
    print("\nExpected local exposure while this script is running:")
    print("  18080 -> OPEN")
    print("  19090 -> OPEN")
    print("  20001 -> OPEN")
    print("  20002 -> should be CLOSED unless another local program is using it")
    print("\nPress Ctrl+C to stop all local test services.")
    try:
        while True:
            threading.Event().wait(60)
    except KeyboardInterrupt:
        print("\nStopping local test services.")

if __name__ == "__main__":
    main()
