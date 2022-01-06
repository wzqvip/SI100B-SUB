import time,machine


#四个光敏电阻的电压
light_sensor1=machine.ADC(machine.Pin(13)) #上
light_sensor2=machine.ADC(machine.Pin(12)) #下
light_sensor3=machine.ADC(machine.Pin(14)) #右
light_sensor4=machine.ADC(machine.Pin(27)) #左

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

    
def main_loop():
    try:
        while True:
            main_control()
            # main_display0()
            time.sleep(1)


    except:
        print("main_loop end")
        servo1.deinit()
        servo2.deinit()


main_loop()