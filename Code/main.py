from machine import Pin, PWM, ADC, I2C
import ssd1306
import math
import time
from servo import Servo


# Servo setup
#servo_x = PWM(Pin(15))  # Servo for X-axis connected to GP15
#servo_y = PWM(Pin(16))  # Servo for Y-axis connected to GP16
#servo_2y = PWM(Pin(16))  # Servo for Y-axis connected to GP16
#servo_x.freq(50)
#servo_y.freq(50)
#servo_2y.fer(50)
Xservo = Servo(pin_id=15)
Yservo = Servo(pin_id=16)
YYservo = Servo(pin_id=17)

           
# Joystick setup
VRXpin = ADC(26)  # Joystick X-axis
VRYpin = ADC(27)  # Joystick Y-axis
SWpin = Pin(2, Pin.IN, Pin.PULL_UP)  # Joystick button                                                                                                                             

# OLED setup
oled_width = 128
oled_height = 64
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

#initial value
shiftX = 0
shiftY = 0
Xservo.write(0)
Yservo.write(0)
YYservo.write(180)

#Ranges of Joystick: [0, 65535]
#Range of Servos: [0, 180]
def convertVal(jsVal):
    return jsVal * (110 / 65535)


while True:
    Xval = VRXpin.read_u16()
    Yval = VRYpin.read_u16()
    SW = SWpin.value()
    
    shiftX = convertVal(Xval)
    shiftY = convertVal(Yval)
    
    Xservo.write(shiftX)
    Yservo.write(shiftY)
    YYservo.write(180 - shiftY)
    
    # Update OLED display
    oled.fill(0)
    oled.text('ServoX Pos:', 0, 0) 
    oled.text(str(shiftX), 89, 0)
    oled.text('ServoY Pos:', 0, 20)
    oled.text(str(shiftY), 89, 20)
    oled.show()
    
    if (SW == 0):
        while (SW == 0):
            oled.fill(0)
            oled.text('Joystick Pressed!', 0, 30)
            oled.text('ServoSW val:', 0, 40)
            oled.text(str(SW), 100, 40)
            oled.show()
            SW = SWpin.value()
        
    oled.show()

    time.sleep_ms(200)
 

