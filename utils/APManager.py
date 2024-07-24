import network


class APManager:
    def __init__(self, name='ESP32_AP', password="123456789"):
        self.essid = name
        self.password = password

    def enable(self):
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(authmode=network.AUTH_WPA_WPA2_PSK, essid=self.essid, password=self.password)