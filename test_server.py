import _thread
import socket

import json
import sys


class HTTPServer:
    def __init__(self):
        self.server_socket = None
        self.max_connection = 5  # 最大连接数
        self.max_run_time = 6

        self.route_map = {
            "/": {"func": lambda x: "root_path", "method": "POST"},
            "/test": {"func": lambda x: "This is a test route.", "method": "POST"},
        }
        # self.start(host, port)

    def start(self, host, port):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((host, port))
            self.server_socket.listen(self.max_connection)
        except:
            print("bind error")
            sys.exit(1)

        while True:
            client_socket, client_address = self.server_socket.accept()

            self.max_run_time -= 1
            if self.max_run_time < 0:
                sys.exit(1)
            _thread.start_new_thread(self.handle_request, (client_socket, client_address))

    def handle_request(self, client_socket, client_address):
        print(f"client_address={client_address}")
        request = client_socket.recv(1024).decode('utf-8')
        headers, body = request.split('\r\n\r\n', 1)
        header_lines = headers.split('\r\n')
        method, path, _ = header_lines[0].split(' ')

        try:
            if method == 'POST':
                url_path = path
                content_length = int([line.split(': ')[1] for line in header_lines if 'Content-Length' in line][0])
                payload = json.loads(body[:content_length])  # todo:unsafe
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
            resp_route = self.route_map.get(url_path)
            if resp_route:
                response_body = resp_route["func"](payload)
            else:
                response_body = "404 Not Found"
        except:
            response_body = "server internel error"
        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"

        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()
        print("req done -----")

    def add_route(self, path, callback_func, method):
        self.route_map.update({path: {"func": callback_func, "method": method}})


if __name__ == '__main__':
    server = HTTPServer()
