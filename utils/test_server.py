import socket


class HTTPServer:
    # route_map = {route: {"func": func, "method":method}}
    route_map = {}

    def __init__(self, host='127.0.0.1', port=8080):
        self.server_socket = None
        self.max_connection = 5  # 最大连接数
        self.start(host, port)

    def start(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(self.max_connection)
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"client_address={client_address}")
            request = client_socket.recv(1024).decode('utf-8')

            # content_length = int([h.split(': ')[1] for h in headers if 'Content-Length' in h][0])
            # body = client_socket.recv(content_length).decode('utf-8')
            # print(f"body={body}")

            response = self.handle_request2(request)
            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()

    def handle_request(self, request):
        headers = request.split('\n')
        method, path, _ = headers[0].split()
        print(f"method={method}, path={path}")
        if method == 'GET':
            if path == '/':
                return 'HTTP/1.1 200 OK\n\nHello, World!'
            elif path == '/about':
                return 'HTTP/1.1 200 OK\n\nThis is the about page.'
            else:
                return 'HTTP/1.1 404 NOT FOUND\n\nPage Not Found'
        else:
            return 'HTTP/1.1 405 METHOD NOT ALLOWED\n\nMethod Not Allowed'

    def handle_request2(self, request):

        headers, body = request.split('\r\n\r\n', 1)
        header_lines = headers.split('\r\n')
        method, path, _ = header_lines[0].split(' ')

        # 解析 URL 和查询参数
        # url = urlparse(path)
        # query_params = parse_qs(url.query)
        print(f"path={path}")

        # 解析 POST 数据
        if method == 'POST':
            content_length = int([line.split(': ')[1] for line in header_lines if 'Content-Length' in line][0])
            post_params = body[:content_length]
        else:
            post_params = {}

        # 打印解析后的参数
        print(f"Method: {method}")
        print(f"Path: {path}")
        print(f"Post Params: {post_params}")

        # 根据路由返回不同的响应
        if path == '/':
            response_body = "Hello, World!"
        elif path == '/test':
            response_body = "This is a test route."
        else:
            response_body = "404 Not Found"

        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"
        return response

    @classmethod
    def add_route(cls, path, callback_func, method):
        cls.route_map.update({path: {"func": callback_func, "method": method}})


if __name__ == '__main__':
    server = HTTPServer()