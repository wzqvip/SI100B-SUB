
import time
import machine

servo = machine.PWM(machine.Pin(15),50)
servo1 = machine.PWM(machine.Pin(2),50)

try:                       #The catching
  while True:
    servo.duty(26)
    time.sleep(1)
    servo1.duty(26)
    time.sleep(1)
    servo.duty(128)
    time.sleep(1)
    servo1.duty(128)
    time.sleep(1)
except:                    #Capture anomaly, deinit Timer and PWM
    servo.deinit()
    servo1.deinit()


