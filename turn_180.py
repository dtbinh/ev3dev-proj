#!/usr/bin/python

from ev3dev.ev3 import LargeMotor as LargeMotor
from time import sleep

b = LargeMotor(address='outB')
c = LargeMotor(address='outC')

b.reset()
c.reset()

b.position_sp = 150
c.position_sp = -150

b.duty_cycle_sp = 50
c.duty_cycle_sp = -50

b.command = 'run-to-abs-pos'
c.command = 'run-to-abs-pos'

sleep(3)
