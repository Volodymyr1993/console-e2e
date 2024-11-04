import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl


class ReqHandler(BaseHTTPRequestHandler):
    def version_string(self):
        return 'CoolHttp/1.0'

    def do_GET(self):
        msg = f'GET {self.path}\n{self.headers}'
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.send_header('Content-length', str(len(msg)))
        self.end_headers()
        self.wfile.write(msg.encode())


def run(port, tls):
    httpd = HTTPServer(('0.0.0.0', port), ReqHandler)
    if tls:
        httpd.socket = ssl.wrap_socket(
            httpd.socket,
            certfile=tls,
            server_side=True)
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a simple HTTP server')
    parser.add_argument(
        '-p',
        dest='port',
        type=int,
        default=443,
        help='Specify the port on which the server listens',
    )
    parser.add_argument(
        '-tls',
        dest='tls',
        default='./certs/self-signed.pem',
        help='Specify the TLS certificate file',
    )

    args = parser.parse_args()
    run(port=args.port, tls=args.tls)
