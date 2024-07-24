# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import time

from utils.HTTPServer import HTTPServer
from utils.Light import Lighter
from utils.WiFiManager import WiFiConnector

wifi_ssid = "gongguisong"
wifi_pwd = "gongguisong"

wifi = WiFiConnector()
lighter = Lighter()

lighter.blink(0.3)
print("searching...")
while not wifi.check_wifi_exist(wifi_ssid):
    time.sleep(1)
    print(f"WIFI:[{wifi_ssid}]not found")

print("connecting...")
lighter.blink(1)
wifi.connect_wifi(wifi_ssid, wifi_pwd)
ip, mask, gateway, dns = wifi.get_config()
print(ip)
print("connected")
lighter.off()

server = HTTPServer()
server.add_route(path="/ttt", callback_func=lambda x: "Hello, World!", method="POST")
server.start(host='127.0.0.1', port=80)
