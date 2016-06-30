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
        self.speed_cap = 75
        self.negative_speed_cap = self.speed_cap * -1

        self.normal_speed = 0
        self.speed_b = 0
        self.speed_c = 0
        self.direction = 'straight'

        self.motor_b = ev3.LargeMotor(address='outB')
        self.motor_b.reset()
        self.motor_b.duty_cycle_sp = self.normal_speed
        self.motor_b.command = 'run-direct'

        self.motor_c = ev3.LargeMotor(address='outC')
        self.motor_c.reset()
        self.motor_c.duty_cycle_sp = self.normal_speed
        self.motor_c.command = 'run-direct'

        self.turn_motor = ev3.MediumMotor()
        self.turn_motor.reset()
        self.turn_motor.duty_cycle_sp = 50
        self.turn_motor.time_sp = 100

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


            self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
            self.state = self.wm.state
            self.acc = self.state['acc']
            self.buttons = self.state['buttons']

            if self.buttons == buttons.plus:
                self.mode =  'Easy'
            elif self.buttons == buttons.minus:
                self.mode = 'Hard'
            elif self.buttons == buttons.a:
                self.mode = 'Turn'
            elif self.buttons == buttons.home:
                exit()

            if self.mode == 'Easy':
                powers = self.Easy_Control()
            elif self.mode == 'Hard':
                powers = self.Hard_Control()
            elif self.mode == 'Turn':
                powers = self.Quick_Turn()

            self.motor_b.duty_cycle_sp = powers[0]
            self.motor_c.duty_cycle_sp = powers[1]

            sleep(0.1)



    def Easy_Control(self):

        if self.buttons == buttons.two:
            if self.turn_motor.position > 10:
                self.turn_motor.position_sp = -25
            elif self.turn_motor.position < -10:
                self.turn_motor.position_sp = 25
            else:
                self.turn_motor.position_sp = 0
            self.speed_b -= 10
            self.speed_c -= 10
        elif self.buttons == buttons.one:
            if self.turn_motor.position > 10:
                self.turn_motor.position_sp = -25
            elif self.turn_motor.position < -10:
                self.turn_motor.position_sp = 25
            self.speed_b += 10
            self.speed_c += 10
        elif self.buttons == buttons.two + buttons.right:
            self.turn_motor.position_sp = -25
            self.speed_b -= 10
            self.speed_c -= 10
        elif self.buttons == buttons.two + buttons.left:
            self.turn_motor.position_sp = 25
            self.speed_b -= 10
            self.speed_c -= 10
        elif self.buttons == buttons.one + buttons.right:
            self.speed_b += 10
            self.speed_c += 10
            self.turn_motor.position_sp = -25
        elif self.buttons == buttons.one + buttons.left:
            self.speed_b += 10
            self.speed_c += 10
            self.turn_motor.position_sp = 25
        else:
            self.speed_b = 0
            self.speed_c = 0



        if self.speed_b >= self.speed_cap:
            self.speed_b = self.speed_cap
        if self.speed_c >= self.speed_cap:
            self.speed_c = self.speed_cap
        if self.speed_b <= self.negative_speed_cap:
            self.speed_b = self.negative_speed_cap
        if self.speed_c <= self.negative_speed_cap:
            self.speed_c = self.negative_speed_cap

        if self.turn_motor.position + self.turn_motor.position_sp < 50 and self.turn_motor.position + self.turn_motor.position_sp > -50:
            self.turn_motor.command = 'run-to-rel-pos'

        return(self.speed_b, self.speed_c)



    def Hard_Control(self):


        #self.turn_power = 0
        #self.correction = 0

        if self.buttons == buttons.two:
            self.speed += 10
        elif self.buttons == buttons.one:
            self.speed -= 10
        else:
            self.speed = 0

        if self.acc[1] != 120:
            if self.acc[1] > 120:
                self.direction = 'left'
            else:
                self.direction = 'right'
        else:
            self.direction = 'straight'

        self.turn_power = 120 - self.acc[1]
        if self.turn_power < 0:
            self.turn_power = self.turn_power * -1

        self.correction = float(self.turn_power * 3) / 100
        self.correction = 1 - self.correction

        if self.direction == 'left':
            self.speed_b = self.speed
            self.speed_c = self.speed * self.correction
        elif self.direction == 'right':
            self.speed_b = self.speed * self.correction
            self.speed_c = self.speed
        elif self.direction == 'straight':
            self.speed_b = self.speed
            self.speed_c = self.speed
        else:
            print("Speed calc error.")

        if self.speed_b >= self.speed_cap:
            self.speed_b = self.speed_cap
        if self.speed_c >= self.speed_cap:
            self.speed_c = self.speed_cap
        if self.speed_b <= self.negative_speed_cap:
            self.speed_b = self.negative_speed_cap
        if self.speed_c <= self.negative_speed_cap:
            self.speed_c = self.negative_speed_cap

        return(self.speed_b, self.speed_c)


    def Quick_Turn(self):

        if self.buttons == buttons.a:
            self.speed_b = 50
            self.speed_c = -50
        else:
            self.speed_b = 0
            self.speed_c = 0

        return(self.speed_b, self.speed_c)



if __name__ == '__main__':

    Main()
