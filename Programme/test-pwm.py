import machine
import time

testpwm1 = machine.PWM(machine.Pin(13),50)
testpwm2 = machine.PWM(machine.Pin(12),50)

print(testpwm1.freq())
print(testpwm2.freq())


