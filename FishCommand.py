from adafruit_motorkit import MotorKit
import sys

kit = MotorKit()
motor = int(sys.argv[1])
throttle = float(sys.argv[2])


if motor==1:
        kit.motor1.throttle = throttle
elif motor==2:
        kit.motor2.throttle = throttle
