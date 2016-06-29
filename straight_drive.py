#!/usr/bin/python

from ev3dev.ev3 import LargeMotor as LargeMotor
from ev3dev.ev3 import TouchSensor as TouchSensor
from time import sleep

power = -100
run_time = 3

motor_b = LargeMotor(address='outB')
motor_c = LargeMotor(address='outC')

motor_b.reset()
motor_c.reset()

motor_b.command = 'run-direct'
motor_c.command = 'run-direct'



trigger = TouchSensor()

print("Fire when ready!")

while True:
    if trigger.value() == True:
        break
    else:
        sleep(.01)


motor_b.duty_cycle_sp = power
motor_c.duty_cycle_sp = power

sleep(run_time)

motor_b.duty_cycle_sp = 0
motor_c.duty_cycle_sp = 0

sleep(1)
