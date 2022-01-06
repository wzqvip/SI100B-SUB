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

from machine import PWM,Pin,ADC
import time

def angle_transefer(angle):
    return int(angle/3.6+26)

servo1 = PWM(Pin(15),50)
#servo2 = PWM(Pin(2),50)

light0 = machine.ADC(machine.Pin(13))  #上面的光敏电阻
light1 = machine.ADC(machine.Pin(12))  #下面的光敏电阻
light2 = machine.ADC(machine.Pin(14))  #右边的光敏电阻
light3 = machine.ADC(machine.Pin(27))  #左边的光敏电阻

def read():
    diff = light0.read()-light1.read()
    return diff

try:
    servo1.duty(26)
    angle1 = 0
    while True:
        #init
        angle1 += read()/10
        if angle1 >= 360:
            angle1 = 360
        elif angle1 <= 0:
            angle1 = 0
        servo1.duty(angle_transefer(angle1))
        print(light0.read(),light1.read(),angle1)
        time.sleep(0.1)
except:
    servo1.deinit()