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



import machine
import time
import network
from umqtt import simple as mqtt
import _thread
import ujson


###阿里云IOT平台接入

ALINK_PROP_SET_METHOD='thing.service.property.set'  #阿里云的东西

def threadPublish():    #发布信息
    while True:
        time.sleep(2)
        # d.measure()
        # print(d.humidity())
        # print(d.temperature())
        # send_mseg={"params":{"Temperature":d.temperature(),"Humidity":d.humidity()},"method":"thing.service.property.set"}
        client.publish(topic=" ",msg=str(send_mseg),qos=1,retain=False)

def receiveMessage():   #接收信息
    while True:
        client.wait_msg()
#接收信息。接收到的信息是json格式，要进行解析。
def recvMessage(topic,msg):   #接收信息
    # parsed=ujson.loads(msg)
    # str=parsed["params"]
    # print(str)
    # print(type(parsed["params"]))
    # print(str.get("PowerSwitch"))
    # global state        
    # state=str.get("PowerSwitch")
    # if state == 1:
    #     led.value(1)
    #     print("led on!") 
    # if state == 0:
    #     led.value(0)
    #     print("led off!")

wlan=network.WLAN(network.STA_IF)  
wlan.active(True)
wlan.connect('HUAWEI Mate 40 Pro+','20020926')#连接WIFI
ProductKey='gowkbf7kwnu'
DeviceName='FNCSAGXVbwdR6kuQ'
DeviceSecret='信导期末项目'
CLIENT_ID='esp32'
user_name='wzqvip'#用户名
user_password='20020926Wang'#用户密码
SERVER= "https://iot.console.aliyun.com/product/productDetail/gowkbf7kwnu"#阿里云物联网平台地址
PORT=1883
client = mqtt.MQTTClient(client_id=CLIENT_ID, server=SERVER, port=PORT, user=user_name, password=user_password, keepalive=60)
client.connect()
client.set_callback(recvMessage)#设置回调函数
client.subscribe(" ")#订阅主题


###主程序部分

#先来读取电压吧
def voltage_transfer(voltage):
    return voltage/1024*3.3

#四个光敏电阻的电压
light_sensor1=machine.ADC(machine.Pin(13))
light_sensor2=machine.ADC(machine.Pin(12))
light_sensor3=machine.ADC(machine.Pin(14))
light_sensor4=machine.ADC(machine.Pin(27))

#把12设置为上下,34设置为左右
analog_diff_up_and_down=light_sensor1-light_sensor2
analog_diff_left_and_right=light_sensor3-light_sensor4

#这里写一个速度控制吧,电压不管了
def speed_calculate(diff):
    if -100<diff<100:
        return 0
    else :
        return diff/100

###舵机控制部分
angle1 = 90  #舵机1初始位置
angle2 = 90  #舵机2初始位置

servo1 = machine.DAC(machine.Pin(15))
servo2 = machine.DAC(machine.Pin(2))

def angle_to_pwm(angle):
    return int(angle*10/180+1500)

def servo_move_to(angle,servo):
    servo.write(angle_to_pwm(angle))

def servo_control(servo,speed):
    global angle1,angle2
    if servo == 1:
        servo_move_to(angle1+speed,servo1)
        angle1 = angle1+speed
    if servo == 2:
        servo_move_to(angle2+speed,servo2)
        angle2 = angle2+speed
    else:
        print("No motor")

###接下来是oled屏幕显示
