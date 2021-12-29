#SI100B 期末project-太阳能追踪
#舵机控制实现追踪
#光敏电阻读取电压比对方位
#IOT平台接入
#oled屏幕显示电压电流,方位等

#引脚说明:
#光敏电阻引脚: IO13 12 14 27
#舵机控制引脚: IO15 2
#oled屏幕引脚: IO16 17
#太阳能电压  : IO25
#太阳能电流  : IO26
#变压输出电压: IO33
#变压输出电流: IO32

###数据标定:
#光敏电阻-10k
#环境光300内,直射2000+



import machine
import time
#import ssd1306


"""这里是发布信息"""
# from simple import MQTTClient
# import network
# from machine import Pin,Timer


# print("import ok")

# SSID="********"
# PASSWORD="*******"
 
# SERVER ='106.15.83.29'#这里使用域名一直连接不上，只能转换为IP使用了
# #PORT：端口号，库里面默认使用处理
# CLIENT_ID = "7788|securemode=3,signmethod=hmacsha1|"   #设备ID
# username='ESP32-Device1&a1R00eqY67d'
# password='0A1457C700FBEFE108B3E5E5523777BA82321363'
 
# publish_TOPIC = '/sys/a1R00eqY67d/ESP32-Device1/thing/event/property/post'
# subscribe_TOPIC ='/sys/a1R00eqY67d/ESP32-Device1/thing/event/property/post_reply'
 
# client=None
# mydht=None
# def sub_cb(topic, msg):
#     print((topic, msg))
 
# def ConnectWifi(ssid,passwd):
#     global wlan
#     wlan=network.WLAN(network.STA_IF)         #create a wlan object
#     wlan.active(True)                         #Activate the network interface
#     wlan.disconnect()                         #Disconnect the last connected WiFi
#     wlan.connect(ssid,passwd)                 #connect wifi
#     while(wlan.ifconfig()[0]=='0.0.0.0'):
#         time.sleep(1)
#     print(wlan.ifconfig())
 
# def apptimerevent(mytimer):
#     try:
#         sensordata=ReadData()
#         mymessage='{"params": {"CurrentTemperature": %d ,"CurrentHumidity": %d }, "method": "thing.event.property.post"}'%(sensordata[0],sensordata[1])
#         client.publish(topic=publish_TOPIC,msg= mymessage, retain=False, qos=0)
#     except Exception as ex_results2:
#         print('exception',ex_results2)
#         mytimer.deinit()
# #     finally:
# #         machine.reset()
 
# def ReadData():
    
#     tem= '数据1'
#     hum= 'data2'
#     data=[tem,hum]
#     print(data)
    
#     return data
    
# if __name__=='__main__':
#     try:
        
#         ConnectWifi(SSID,PASSWORD)
#         client = MQTTClient(CLIENT_ID, SERVER,0,username,password,60)     #create a mqtt client
#         print(client)
#         client.set_callback(sub_cb)                         #set callback
#         client.connect()                                    #connect mqtt
#         client.subscribe(subscribe_TOPIC)                   #client subscribes to a topic
#         mytimer=Timer(0)
#         mytimer.init(mode=Timer.PERIODIC, period=5000,callback=apptimerevent)
#         while True:
#             client.wait_msg()                            #wait message
            
#     except Exception  as ex_results:
#         print('exception1',ex_results)
#     finally:
#         if(client is not None):
#             client.disconnect()
#         wlan.disconnect()
#         wlan.active(False)

"""这里是接收信息的"""
# import LinkNet
# from umqtt.simple import MQTTClient
# from machine import Pin,Timer
# import json




# TOPIC = '/sys/a1WjLnyZ7pi/led_00/thing/service/property/set'
# clientId = '123456'
# ProductKey = 'a1WjLnyZ7pi'
# DeviceName = "led_00"
# DeviceSecret = "wQg7AsfssdMZwsK5JMP8b3D2JM8curRg"
# CLIENT_ID = clientId+"|securemode=3,signmethod=hmacsha1,timestamp=789|"
# user_name = DeviceName+"&"+ProductKey
# user_password = '7836ea60e600589478251396c3117ab10305080a'
# SERVER = ProductKey + ".iot-as-mqtt.cn-shanghai.aliyuncs.com"
# PORT = 1883
# # 都是从阿里云IoT中获得的配置信息
# led = Pin(2, Pin.OUT, value=1)
# client = MQTTClient(client_id=CLIENT_ID, server=SERVER, port=PORT, user=user_name, password=user_password, keepalive=60)



# def MQTT_Send(tim):
#     #发布信息
#     send_mseg = {"params":
#                         {"alive": 1 },
#                 "method": "thing.event.property.post"}

#     client.publish(topic="/sys/a1WjLnyZ7pi/led_00/thing/event/property/post",
#                     msg=str(send_mseg),qos=1, retain=False)

# def sub_cb(topic, msg):
#     global state
#     msg = json.loads(msg)
#     print((topic, msg))
#     if msg['params']['LightSwitch'] == 0:
#         led.value(0)
#         state = 1
#     elif msg['params']['LightSwitch'] == 1:
#         led.value(1)
#         state = 0

# def heartbeat():
#     tim = Timer(-1)
#     tim.init(period=60000, mode=Timer.PERIODIC,callback=MQTT_Send)  

# def main():
#     LinkNet.linkNet()
#     client.set_callback(sub_cb)
#     client.connect()
#     client.subscribe(TOPIC)
#     print("Connected to %s, subscribed to %s topic" % (SERVER, TOPIC))
#     heartbeat()
#     try:
#         while True:
#             client.wait_msg()
#     finally:
#         client.disconnect()










#四个光敏电阻的电压
light_sensor1=machine.ADC(machine.Pin(13))
light_sensor2=machine.ADC(machine.Pin(12))
light_sensor3=machine.ADC(machine.Pin(14))
light_sensor4=machine.ADC(machine.Pin(27))

sensor1_voltage= light_sensor1.read()
sensor2_voltage= light_sensor2.read()
sensor3_voltage= light_sensor3.read()
sensor4_voltage= light_sensor4.read()
print("read ok")
#把12设置为上下,34设置为左右
analog_diff_up_and_down=sensor1_voltage-sensor2_voltage
analog_diff_left_and_right=sensor3_voltage-sensor4_voltage

#这里写一个速度控制吧,电压不管了
def speed_calculate(diff):
    if -100<diff<100:
        return 0
    else :
        return diff/100

###舵机控制部分
global angle1,angle2
angle1 = 90  #舵机1初始位置
angle2 = 90  #舵机2初始位置
#servo1,angle1
#servo2,angle2
servo1=machine.PWM(machine.Pin(15),50)
servo2=machine.PWM(machine.Pin(2),50)
print("servo init ok")
def angle_to_pwm(angle):
    return int(angle/3.6+26)

def servo_move_to(angle,servo):
    servo.duty(angle_to_pwm(angle))

def servo_control(servo,speed):
    global angle1,angle2
    if servo == servo1:
        angle1 += speed
        if angle1 > 180:  #极限复位
            angle1 = 0
            time.sleep(2)
        if angle1 < 0:
            angle1 = 180
            time.sleep(2)
        servo_move_to(angle1,servo)
    if servo == servo2:
        angle2 += speed
        if angle2 > 180:   #这里没啥,防止报错用的
            angle2 = 180
        elif angle2 < 0:
            angle2 = 0
        servo_move_to(angle2,servo)


# ###接下来是oled屏幕显示
# oled_pins = machine.I2C(scl=machine.Pin(16), sda=machine.Pin(17), freq=100000)
# oled_display = ssd1306.SSD1306_I2C(128, 64, oled_pins)
# print("oled init ok")
# def display_oled(text1,text2,text3,text4):
#     oled_display.text(text1, 0, 0)
#     oled_display.text(text2, 0, 10)
#     oled_display.text(text3, 0, 20)
#     oled_display.text(text4, 0, 30)
#     oled_display.show()

#oled_display.invert(True)  #反色显示

##然后是一些简易的电压换算之类的.

sun_voltage=machine.ADC(machine.Pin(25))
sun_current=machine.ADC(machine.Pin(26))
stable_voltage=machine.ADC(machine.Pin(33))
stable_current=machine.ADC(machine.Pin(32))

print("adc init ok")
def voltage_transfer(voltage):
    return voltage/1024*3.3

def read_voltage_sun():
    return voltage_transfer(sun_voltage.read())
    
def read_current_sun():
    return voltage_transfer(sun_current.read())*1000/185  #单位换算: 185mv/A

def read_voltage_stable():
    return voltage_transfer(stable_voltage.read())

def read_current_stable():
    return voltage_transfer(stable_current.read())*1000/185  #单位换算: 185mv/A


###主程序?
def main_control():
    print("running main")
    #首先确认旋转方向
    global angle1,angle2
    speed1=speed_calculate(analog_diff_left_and_right)
    speed2=speed_calculate(analog_diff_up_and_down)
    #然后是电机控制
    servo_control(servo1,speed1)
    servo_control(servo2,speed2)

# def main_display0():
#     print("running display0")
#     global angle1,angle2
#     line1 = str("Sun auto follower")
#     line2 = str(angle1+"°"+" "+angle2+"°")
#     line3 = str("V1"+str(read_voltage_sun())+"V"+" I1"+str(read_current_sun())+"A")
#     line4 = str("V2"+str(read_voltage_stable())+"V"+" I2"+str(read_current_stable())+"A")
#     display_oled(line1,line2,line3,line4)

def main_loop():
    try:
        while True:
            main_control()
            # main_display0()
            time.sleep(0.1)


    except:
        print("main_loop end")
        servo1.deinit()
        servo2.deinit()




# _thread.start_new_thread(main_loop,())
# _thread.start_new_thread(client.check_msg,())
# _thread.start_new_thread(client.send_msg,())
main_loop()