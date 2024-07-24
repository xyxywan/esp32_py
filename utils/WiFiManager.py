import network
import time


class WiFiManager:
    def __init__(self):
        try:
            self.wlan = network.WLAN(network.STA_IF)
            self.wlan.active(True)
        except:
            print("err wifi")

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