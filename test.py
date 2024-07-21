import socket


def handle_request(request):
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


def run_server(host='127.0.0.1', port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f'Serving HTTP on {host} port {port} ...')

    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode()
        response = handle_request(request)
        client_socket.sendall(response.encode())
        client_socket.close()


if __name__ == '__main__':
    run_server()
