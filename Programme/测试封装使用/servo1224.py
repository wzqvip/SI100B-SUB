import time
from machine import Pin
from machine import PWM
from machine import ADC

# object construct
# s = servo(pwm, adc0, adc1, minx, maxx) => servo object
# pwm, adc0, adc1 => pin id
# minx = min duty value, maxx = max duty value

# auto run servo
# servo.eventListener(vServo, hServo) => None
# vServo = vertical servo, hServo = horizontal servo

# change config
# servo.config(direct, step, sense, minv)
#   => (direc, step, sense, minv)
# all the parameters are not essential
# direc = direction factor => 1 or -1
# step = duty change factor for each move, smaller is recommended
# sense = sensitivity, smaller means more sensitive
# minv = min value for darkness, larger means darker when return to mid
# default: direc = 1, step = 2, sense = 200, minv = 3800

# manual movement control
# s.modify(nextPosition) => None

# get next position
# s.query() => nextPosition

class servo():
  
    pitch = 1
    direc = 1
    step = 2
    sense = 200
    minv = 3800

    @classmethod
    def config(cls, direc = 1, step = 2, sense = 200, minv = 3800):
        cls.direc = direc
        cls.step = step
        cls.sense = sense
        cls.minv = minv
        return (cls.direc, cls.step, cls.sense, cls.minv)

    def __init__(self, pwm, adcl, adcr, minx, maxx):
        self.pwm = PWM(Pin(pwm), 50)
        self.adcl = ADC(Pin(adcl))
        self.adcr = ADC(Pin(adcr))
        self.min = int(minx)
        self.max = int(maxx)
        self.mid = (self.min + self.max) // 2
        self.cur = self.mid
        self.modify(self.mid)
    
    def getX(self, direct):
        go = 0
        if direct > servo.sense:
            go = servo.step
        elif direct < -servo.sense:
            go = -servo.step
        if self.mid != 77:
            go *= servo.pitch
        return int(self.cur + go)

    def modify(self, x):
        if self.mid == 77:
            if self.cur == self.mid: 
                if x > self.mid:
                    servo.pitch = servo.direc
                else:
                    servo.pitch = -servo.direc
            else:
                if self.cur < self.mid and x > self.mid:
                    servo.pitch = servo.direc
                elif self.cur > self.mid and x < self.mid:
                    servo.pitch = -servo.direc
        self.pwm.duty(x)
        self.cur = x
        time.sleep_ms(50)

    def query(self):
        vl = self.adcl.read()
        vr = self.adcr.read()
        #print(self.mid, vl, vr)
        if min(vl, vr) > servo.minv:
            return self.mid
        else: 
            return self.getX(vl - vr)

    def deinit(self):
        self.pwm.deinit()
        
    @staticmethod 
    def eventListener(vServo, hServo):
        xv = vServo.query()
        xh = hServo.query()
        if vServo.min <= xv <= vServo.max:
            vServo.modify(xv)
        if xh < hServo.min:
            hServo.modify(hServo.max + xh - hServo.min)
            vServo.modify(vServo.mid * 2 - vServo.cur)
            time.sleep(1.1)
        elif xh > hServo.max:
            hServo.modify(hServo.min + xh - hServo.max)
            vServo.modify(vServo.mid * 2 - vServo.cur)
            time.sleep(1.1)
        else: 
            hServo.modify(xh)
