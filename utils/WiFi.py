import network
import time
from Light import Lighter


class WiFiConnector:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

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


if __name__ == '__main__':
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

    print("connected")
    lighter.close()

