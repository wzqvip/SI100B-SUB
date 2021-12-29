import network,webrepl
import time


def GetAPName():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    AP = station.scan()
    APname = [i[0].decode('UTF-8') for i in AP]
    return APname


def linkNet(name,passwd,timeout=3000):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("connecting to network...") 
        sta_if.active(True)
        sta_if.connect(name, passwd)
        while not sta_if.isconnected():
            time.sleep_ms(1)
            if timeout==0:
                sta_if.active(False)
                return "timeout"
            else:
                timeout-=1
    print("network config:", sta_if.ifconfig())
    webrepl.start()
    return "ok"
