import network
import time
import machine
from machine import Pin
import _thread
import _thread
import socket

import json
import sys



class WiFiManager:
    def __init__(self):
        try:
            self.wlan = network.WLAN(network.STA_IF)
            self.wlan.active(True)
        except:
            print("err wifi")
            pass

    def close(self):
        self.wlan.active(False)

    def connect_wifi(self, wifi_ssid, wifi_pwd):
        self.wlan.disconnect()
        self.wlan.connect(wifi_ssid, wifi_pwd)

        for _ in range(10):
            if self.wlan.isconnected():
                return True
            else:
                time.sleep(0.5)
        return False

    def check_wifi_exist(self, wifi_ssid):
        wifi_list = self.wlan.scan()
        for item in wifi_list:
            if wifi_ssid in str(item):
                return True
        return False

    def get_config(self):
        # IP地址、子网掩码、网关和DNS服务器的元组
        ip, mask, gateway, dns = self.wlan.ifconfig()
        return ip, mask, gateway, dns

    def scan(self):
        return self.wlan.scan()


class Lighter:
    def __init__(self, pin_num=2):
        self.light = Pin(pin_num, Pin.OUT)
        self.blinking = False

    def blink(self, interval: float = 1):
        self.blinking = True
        _thread.start_new_thread(self.__internal_blink, (interval,))

    def on(self):
        self.blinking = False
        self.light.value(True)

    def off(self):
        self.blinking = False
        self.light.value(False)

    def __internal_blink(self, interval):
        while self.blinking:
            self.light.value(not self.light.value())
            time.sleep(interval)


class HTTPServer:
    def __init__(self, host, port):
        self.server_socket = None
        self.max_connection = 5  # 最大连接数
        self.max_run_time = 6
        self.host=host
        self.port = port

        self.route_map = {
            "/": {"func": lambda x: "root_path", "method": "POST"},
            "/test": {"func": lambda x: "This is a test route.", "method": "POST"},
        }
        # self.start(host, port)

    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(self.max_connection)
        except:
            print("bind error")
            machine.reset()

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
                ret = resp_route["func"](payload)
                response =self.__handle_result(data=ret, type=resp_route["type"])
            else:
                response = self.__handle_result(data="404 Not Found", type="")
        except:
            response = self.__handle_result(data="server internel error", type="")

        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()
        print("req done -----")

    def add_route(self, path, callback_func, method, type="json"):
        self.route_map.update({path: {"func": callback_func, "method": method, "type": type}})

    def __handle_result(self, data, type="json"):
        if type == "json":
            response_json = json.dumps(data)
            http_response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{response_json}"
        elif type == "html":
            http_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{data}"
        else:
            http_response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(str(data))}\r\n\r\n{data}"
        return http_response



class APManager:
    def __init__(self, name='ESP32_AP', password="123456789"):
        self.essid = name
        self.password = password

    def enable(self):
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(authmode=network.AUTH_WPA_WPA2_PSK, essid=self.essid, password=self.password)

        # self.ap.config(essid=self.essid, password=self.password, authmode=network.AUTH_WPA_WPA2_PSK)

lighter = Lighter()
wifi = WiFiManager()
wifi_list = wifi.scan()
wifi.close()


server = HTTPServer('0.0.0.0', 8080)

lighter.blink(0.3)
ap = APManager()
ap.enable()


def get_wifi_list(req):
    return wifi_list
print(get_wifi_list(None))

server.add_route(path="/wifi", callback_func=get_wifi_list, method="POST")
lighter.on()
#_thread.start_new_thread(server.start, ())
server.start()
