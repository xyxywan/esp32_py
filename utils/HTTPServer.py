import socket

class HTTPServer:
    def __init__(self, host='127.0.0.1', port=8080):
        self.server_socket = None
        self.max_connection = 5   # 最大连接数
        self.start(host, port)

    def start(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(self.max_connection)
        while True:
            client_socket, client_address = self.server_socket.accept()
            request = client_socket.recv(1024).decode()
            response = self.handle_request(request)
            client_socket.sendall(response.encode())
            client_socket.close()

    def handle_request(self, request):
        headers = request.split('\n')
        method, path, _ = headers[0].split()

        if method == 'GET':
            if path == '/':
                return 'HTTP/1.1 200 OK\n\nHello, World!'
            elif path == '/about':
                return 'HTTP/1.1 200 OK\n\nThis is the about page.'
            else:
                return 'HTTP/1.1 404 NOT FOUND\n\nPage Not Found'
        else:
            return 'HTTP/1.1 405 METHOD NOT ALLOWED\n\nMethod Not Allowed'


if __name__ == '__main__':
    server = HTTPServer()
