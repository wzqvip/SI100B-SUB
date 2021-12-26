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


light0 = machine.ADC(machine.Pin(35))
while True:
    print(light0.read())
    time.sleep(0.1)

#环境300上下,直射2000+