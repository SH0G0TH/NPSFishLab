import time
from adafruit_motorkit import MotorKit

kit = MotorKit()
mouthMotor = kit.motor2
headTailMotor = kit.motor1

print("Moving Head")
headTailMotor.throttle = .8
time.sleep(1)
print("Test Reset of Head")
headTailMotor.throttle = -.5
time.sleep(.1)
headTailMotor.throttle = 0
