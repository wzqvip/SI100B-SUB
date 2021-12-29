import LinkNet
from umqtt.simple import MQTTClient
from machine import Pin,Timer
import json




TOPIC = '/sys/a1WjLnyZ7pi/led_00/thing/service/property/set'
clientId = '123456'
ProductKey = 'a1WjLnyZ7pi'
DeviceName = "led_00"
DeviceSecret = "wQg7AsfssdMZwsK5JMP8b3D2JM8curRg"
CLIENT_ID = clientId+"|securemode=3,signmethod=hmacsha1,timestamp=789|"
user_name = DeviceName+"&"+ProductKey
user_password = '7836ea60e600589478251396c3117ab10305080a'
SERVER = ProductKey + ".iot-as-mqtt.cn-shanghai.aliyuncs.com"
PORT = 1883
# 都是从阿里云IoT中获得的配置信息
led = Pin(2, Pin.OUT, value=1)
client = MQTTClient(client_id=CLIENT_ID, server=SERVER, port=PORT, user=user_name, password=user_password, keepalive=60)



def MQTT_Send(tim):
    #发布信息
    send_mseg = {"params":
                        {"alive": 1 },
                "method": "thing.event.property.post"}

    client.publish(topic="/sys/a1WjLnyZ7pi/led_00/thing/event/property/post",
                    msg=str(send_mseg),qos=1, retain=False)

def sub_cb(topic, msg):
    global state
    msg = json.loads(msg)
    print((topic, msg))
    if msg['params']['LightSwitch'] == 0:
        led.value(0)
        state = 1
    elif msg['params']['LightSwitch'] == 1:
        led.value(1)
        state = 0

def heartbeat():
    tim = Timer(-1)
    tim.init(period=60000, mode=Timer.PERIODIC,callback=MQTT_Send)  

def main():
    LinkNet.linkNet()
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(TOPIC)
    print("Connected to %s, subscribed to %s topic" % (SERVER, TOPIC))
    heartbeat()
    try:
        while True:
            client.wait_msg()
    finally:
        client.disconnect()
