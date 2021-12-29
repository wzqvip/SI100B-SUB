from umqtt.simple import MQTTClient
import usocket as socket
import time
import wifi
 
wifi.connect()
 
#Demo_01
ProductKey = "a1Mf4HZ5k**"
ClientId = "1234|securemode=3,signmethod=hmacsha1|"
DeviceName = "Demo_01"
DeviceSecret = "****************************"
 
strBroker = ProductKey + ".iot-as-mqtt.cn-shanghai.aliyuncs.com"
Brokerport = 1883
 
user_name = "Demo_01&a1Mf4HZ5k**"
user_password = "***************************************"
 
print("clientid:",ClientId,"\n","Broker:",strBroker,"\n","User Name:",user_name,"\n","Password:",user_password,"\n")
 
 
def connect():
	client = MQTTClient(client_id = ClientId,server= strBroker,port=Brokerport,user=user_name, password=user_password,keepalive=60) 
	#please make sure keepalive value is not 0
	
	client.connect()
 
	temperature =25.00
	while temperature < 30:
		temperature += 0.5		
	
		send_mseg = '{"params": {"IndoorTemperature": %s},"method": "thing.event.property.post"}' % (temperature)
		client.publish(topic="/sys/a1Mf4HZ5kET/Demo_01/thing/event/property/post", msg=send_mseg,qos=1, retain=False)
		
		time.sleep(3)
 
	while True:
		pass
 
	#client.disconnect()



"""
https://developer.aliyun.com/ask/282972

做的过程中参考了一下链接，放在这里，读者可以阅读，以获得更多细节：

子设备接入

https://help.aliyun.com/document_detail/66641.html

ESP8266 and MicroPython - Part 2

https://www.home-assistant.io/blog/2016/08/31/esp8266-and-micropython-part2/

使用MQTT客户端连接阿里云MQTT服务器

https://yq.aliyun.com/articles/592279

使用Python模拟设备接入阿里云物联网的MQTT服务器

https://yq.aliyun.com/articles/162978


"""