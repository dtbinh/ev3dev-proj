#!/usr/bin/python

import ev3dev.ev3 as ev3
from time import sleep

class Main():

    def __init__(self):

        self.normal_speed = 50

        self.motor_b = ev3.LargeMotor(address='outB')
        self.motor_b.reset
        self.motor_b.duty_cycle_sp = self.normal_speed
        self.motor_b.command = 'run-direct'

        self.motor_c = ev3.LargeMotor(address='outC')
        self.motor_c.reset
        self.motor_c.duty_cycle_sp = self.normal_speed
        self.motor_c.command = 'run-direct'

        self.color = ev3.ColorSensor(address='in3')
        self.color.mode = 'COL-REFLECT'
        self.wanted_value = 50

        self.LineFollow()

    def LineFollow(self):

        while True:

            value = self.color.value()
            error = value - self.wanted_value
            correction = error * .8

            if correction > 100:
                correction = 100
            elif correction < -100:
                correction = -100

            if correction > 0:
                self.motor_b.duty_cycle_sp = correction
                self.motor_c.duty_cycle_sp = self.normal_speed
            elif correction < 0:
                self.motor_c.duty_cycle_sp = correction
                self.motor_b.duty_cycle_sp = self.normal_speed
            elif correction == 0:
                self.motor_b.duty_cycle_sp = self.normal_speed
                self.motor_c.duty_cycle_sp = self.normal_speed
            else:
                print("Error, correction out of range.")

            sleep(.01)



if __name__ == '__main__':

    Main()
