#!/usr/bin/python

from ev3dev.ev3 import MediumMotor as MediumMotor
from ev3dev.ev3 import LargeMotor as LargeMotor
from time import sleep

a = MediumMotor(address='outA')
b = LargeMotor(address='outB')
c = LargeMotor(address='outC')

a.reset()
b.reset()
c.reset()

a.position_sp = 50
a.duty_cycle_sp = 50
a.command = 'run-to-abs-pos'

b.position_sp = -450
b.duty_cycle_sp = 50
b.command = 'run-to-abs-pos'

c.position_sp = -450
b.duty_cycle_sp = 50
b.command = 'run-to-abs-pos'

sleep(5)
