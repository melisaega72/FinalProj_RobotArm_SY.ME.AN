from machine import Pin, I2C
#PWM, ADC, 12C
import ssd1306
import time

# Servo setup
servo_x = PWM(Pin(15))  # Servo for X-axis connected to GP15
servo_y = PWM(Pin(16))  # Servo for Y-axis connected to GP16
servo_x.freq(50)
servo_y.freq(50)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
X = 31;

# Joystick setup
Xpin = ADC(26)  # Joystick X-axis
Ypin = ADC(27)  # Joystick Y-axis
SWpin = Pin(2, Pin.IN, Pin.PULL_UP)  # Joystick button

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def set_servo_angle(servo, angle):
    """Moves the servo to the specified angle (0–180 degrees)."""
    if 0 <= angle <= 180:
        duty = int(2048 + (angle / 180) * 4096)
        servo.duty_u16(duty)

def map_value(value, in_min, in_max, out_min, out_max):
    """Maps a value from one range to another."""
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while True:
     Read joystick inputs
    X = Xpin.read_u16()
    Y = Ypin.read_u16()
    SW = SWpin.value()
  
    #Map joystick inputs to servo angles
    angle_x = map_value(X, 0, 65535, 0, 180)
    angle_y = map_value(Y, 0, 65535, 0, 180)

    # Move servos
    set_servo_angle(servo_x, angle_x)
    set_servo_angle(servo_y, angle_y)

    # Update OLED display
    oled.fill(0)  # Clear the display
    oled.text("Joystick Control", 0, 0)
    oled.text(f"X: {X}", 0, 10)
    oled.text(f"Y: {Y}", 0, 20)
    oled.text(f"Angle X: {angle_x}", 0, 30)
    oled.text(f"Angle Y: {angle_y}", 0, 40)
    oled.text(f"SW: {'Pressed' if SW == 0 else 'Released'}", 0, 50)
    oled.show()

    time.sleep(0.1)

#Need to display the positions of the motors
oled.fill(0)
oled.text('ServoX Pos:', 0, 0)
oled.text('00.00', 89, 0)
oled.text('ServoY Pos:', 0, 20)
oled.text('00.00', 89, 20)

if (X == 31):
    oled.fill(0)
    oled.text('Joystick Pressed!', 0, 30)
    oled.text('ServoSW val:', 0, 40)
    oled.text('0', 100, 40)
    oled.show()

oled.show()

