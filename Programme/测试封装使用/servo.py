
import time
import machine

servo = machine.PWM(machine.Pin(15),50)
#servo1 = machine.PWM(machine.Pin(2),50)

def angle_transfer(angle):
    return int(angle/3.6+26)

try:                       #The catching
  while True:
    angle = angle_transfer(input("please input angle:"))
    servo.duty(angle)
except:                    #Capture anomaly, deinit Timer and PWM
    servo.deinit()
    #servo1.deinit()


