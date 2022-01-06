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

light0 = machine.ADC(machine.Pin(13))  #下面的光敏电阻
light1 = machine.ADC(machine.Pin(12))  #上面的光敏电阻
light2 = machine.ADC(machine.Pin(14))  #左边的光敏电阻
light3 = machine.ADC(machine.Pin(27))  #右边的光敏电阻


servo1 = machine.PWM(machine.Pin(15),50)
servo2 = machine.PWM(machine.Pin(2),50)
 
angle1 = 90  #舵机1初始位置
angle2 = 90  #舵机2初始位置

def angle_to_pwm(angle):
    return int(angle/1.8+26)

try:
    while True:
        time.sleep(0.05)
        print(light0.read(),light1.read(),light2.read(),light3.read())
        angle1 -= int((light3.read()-light2.read())/100)
        angle2 -= int((light1.read()-light0.read())/100)
        print("angle1:",angle1)
        print("angle2:",angle2)
        if angle1 > 180:  
            angle1 = 180
        if angle1 < 0:
            angle1 = 0
        if angle2 > 180:
            angle2 = 180
        if angle2 < 0:
            angle2 = 0
        servo1.duty(angle_to_pwm(angle1))
        servo2.duty(angle_to_pwm(angle2))
except:
    servo1.deinit()
    servo2.deinit()
#环境300上下,直射2000+