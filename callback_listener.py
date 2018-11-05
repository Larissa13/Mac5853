from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver

class SimpleServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>hi!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print("data received by post: \n", post_data)
        self._set_headers()


def run(server_class=HTTPServer, handler_class=SimpleServer, port=5001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting callback listener server')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
