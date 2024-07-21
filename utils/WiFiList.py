# 导入socket模块
import socket

# 创建一个TCP套接字
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 设置套接字选项，允许重用地址
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 绑定到本地地址和端口
s.bind(('0.0.0.0', 80))

# 开始监听连接请求
s.listen(5)

# 循环处理客户端连接
while True:
    # 接受一个客户端连接，并返回一个新的套接字和地址
    conn, addr = s.accept()
    # 接收客户端请求
    request = conn.recv(1024)
    # 打印请求内容
    print(request)
    # 构造响应内容
    response = b'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\nHello, MicroPython!'
    # 发送响应内容
    conn.send(response)
    # 关闭连接
    conn.close()
