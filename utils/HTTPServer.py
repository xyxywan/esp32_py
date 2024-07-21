import _thread
import socket


class HTTPServer:
    # route_map = {route: {"func": func, "method":method}}
    route_map = {}

    def __init__(self, host='127.0.0.1', port=8080):
        self.server_socket = None
        self.max_connection = 5  # 最大连接数
        self.max_run_time = 60
        self.start(host, port)

    def start(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(self.max_connection)
        while self.max_run_time > 0:
            self.max_run_time -= 1
            client_socket, client_address = self.server_socket.accept()
            _thread.start_new_thread(self.handle_request, (client_socket, client_address))

    def handle_request(self, client_socket, client_address):
        print(f"client_address={client_address}")
        request = client_socket.recv(1024).decode('utf-8')
        headers, body = request.split('\r\n\r\n', 1)
        header_lines = headers.split('\r\n')
        method, path, _ = header_lines[0].split(' ')

        if method == 'POST':
            url_path = path
            content_length = int([line.split(': ')[1] for line in header_lines if 'Content-Length' in line][0])
            payload = eval(body[:content_length])  # todo:unsafe
        else:
            payload = {}
            url_path = path
            if "?" in path:
                ret = path.split("?")
                url_path = ret[0]
                content = ret[1].split('&')
                for pair in content:
                    key, value = pair.split('=')
                    payload[key] = value

        # 打印解析后的参数
        print(f"Method: {method}")
        print(f"url_path: {url_path}")
        print(f"payload: {payload}")

        # 根据路由返回不同的响应
        if url_path == '/':
            response_body = "Hello, World!"
        elif url_path == '/test':
            response_body = "This is a test route."
        else:
            response_body = "404 Not Found"

        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"

        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()
        print("req done -----")


    @classmethod
    def add_route(cls, path, callback_func, method):
        cls.route_map.update({path: {"func": callback_func, "method": method}})


if __name__ == '__main__':
    server = HTTPServer()
