#!/usr/bin/python

from wiimod import buttons
from time import sleep
import cwiid
import ev3dev.ev3 as ev3

class Main():

    def __init__(self):

        self.wm = None
        self.number = 6
        self.mode = 'Easy'

        self.normal_speed = 0
        self.speed_b = 0
        self.speed_c = 0

        self.motor_b = ev3.LargeMotor(address='outB')
        self.motor_b.reset
        self.motor_b.duty_cycle_sp = self.normal_speed
        self.motor_b.command = 'run-direct'

        self.motor_c = ev3.LargeMotor(address='outC')
        self.motor_c.reset
        self.motor_c.duty_cycle_sp = self.normal_speed
        self.motor_c.command = 'run-direct'

        self.Connect()
        self.Control_Mode()

    def Connect(self):
        try:
            print("Press 1+2 on the Wiimote now.")
            self.wm = cwiid.Wiimote()
            print("Connected.")
        except RuntimeError:
            print("Error opening wiimote connection")
            exit()

        #set Wiimote to report button presses and accelerometer state
        self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

        #turn on led to show connected
        self.wm.led = self.number

        sleep(1)

    def Control_Mode(self):
        while True:

            self.state = self.wm.state
            self.buttons = self.state['buttons']

            if self.buttons == buttons.plus:
                self.mode =  'Easy'
            elif self.buttons == buttons.minus:
                self.mode = 'Hard'

            if self.mode == 'Easy':
                self.Easy_Control()
            elif self.mode == 'Hard':
                self.Hard_Control

    def Easy_Control(self):


        self.state = self.wm.state
        self.buttons = self.state['buttons']

        if self.buttons == buttons.two:
            self.speed_b += 10
            self.speed_c += 10
        elif self.buttons == buttons.one:
            self.speed_b -= 10
            self.speed_c -= 10
        elif self.buttons == buttons.two + buttons.right:
            self.speed_b -= 5
            self.speed_c = 50
        elif self.buttons == buttons.two + buttons.left:
            self.speed_b = 50
            self.speed_c -= 5
        elif self.buttons == buttons.one + buttons.right:
            self.speed_b += 5
            self.speed_c = -50
        elif self.buttons == buttons.one + buttons.left:
            self.speed_b = -50
            self.speed_c += 5
        elif self.buttons == buttons.home:
            exit()
        else:
            self.speed_b = 0
            self.speed_c = 0

        if self.speed_b >= 100:
            self.speed_b = 100
        if self.speed_c >= 100:
            self.speed_c = 100
        if self.speed_b <= -100:
            self.speed_b = -100
        if self.speed_c <= -100:
            self.speed_c = -100

        self.motor_b.duty_cycle_sp = self.speed_b
        self.motor_c.duty_cycle_sp = self.speed_c

        sleep(.1)

    def Hard_Control(self):



        self.state = self.wm.state
        self.acc = self.state['acc']
        self.buttons = self.state['buttons']

        if self.buttons == buttons.two:
            self.speed += 10
        elif self.buttons == buttons.one:
            self.speed -= 10
        elif self.buttons == buttons.home:
            exit()
        else:
            self.speed = 0

        if self.acc[1] != 123:
            if self.acc[1] > 123:
                self.direction = "left"
            elif self.acc[1] < 123:
                self.direction = "right"
            else:
                direction = "straight"

            if self.direction != "straight" and self.speed != 0:
                if self.acc[1] > 200 and self.direction == "left":
                    self.power_b = 100
                    self.power_c = 0
                elif self.acc[1] < 0 and self.direction == "right":
                    self.power_b = 0
                    self.power_c = 100
                elif self.acc[1] < 200 and self.direction == "left":
                    self.calc = (self.acc[1] - 120) / 50.0
                    if self.calc < 0:
                        self.calc = 0
                    self.power_b = self.calc * (self.speed - 20)
                    if self.power_b >= 100:
                        self.power_b = 0
                    self.power_c = self.speed
                elif self.acc[1] > 0 and self.direction == "right":
                    self.power_b = self.speed
                    self.calc = (self.acc[1] - 120) / 50.0
                    if self.calc < 0:
                        self.calc = 0
                    self.power_c = self.calc * (self.speed - 20)
        else:
            self.power_b = self.speed
            self.power_c = self.speed




        if self.speed_b >= 100:
            self.speed_b = 100
        if self.speed_c >= 100:
            self.speed_c = 100
        if self.speed_b <= -100:
            self.speed_b = -100
        if self.speed_c <= -100:
            self.speed_c = -100

        self.motor_b.duty_cycle_sp = self.speed_b
        self.motor_c.duty_cycle_sp = self.speed_c

        print(self.speed_b)
        print(self.speed_c)

        sleep(.1)




if __name__ == '__main__':

    Main()
