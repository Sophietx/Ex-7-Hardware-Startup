
#os.environ['DISPLAY'] = ":0.0"
#os.environ['KIVY_WINDOW'] = 'egl_rpi'
import pygame
import os

from pidev.Joystick import Joystick

from kivy.clock import Clock
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.uix.slider import Slider

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from kivy.uix.image import Image
from kivy.animation import Animation


from datetime import datetime

from dpeaDPi.DPiStepper import DPiStepper
from dpeaDPi.DPiComputer import *


import threading
from time import sleep



time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
FIRST_SCREEN_NAME = 'first'
SECOND_SCREEN_NAME = 'second'
THIRD_SCREEN_NAME = 'third'

class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER

button_toggle = False

dpiStepper = DPiStepper()
dpiStepper.setBoardNumber(0)


Window.clearcolor = (1, 1, 1, 1)  # White

class FirstScreen(Screen):
    def whatsgoingon(self, button):

        global StepperDirection

        if button.text == 'on':
            if dpiStepper.initialize() != True:
                print("Communication with the DPiStepper board failed.")
                return
            StepperDirection = True
            dpiStepper.enableMotors(True)
            threading.Thread(target=self.spinDirection, args=(button,), daemon=True).start()

        elif button.text == 'off':
            if dpiStepper.initialize() != True:
                print("Communication with the DPiStepper board failed.")
                return
            print('disabling motors')
            dpiStepper.enableMotors(False)

        elif button.text == 'change direction':
            if dpiStepper.initialize() != True:
                print("Communication with the DPiStepper board failed.")
                return
            dpiStepper.enableMotors(True)
            if StepperDirection == True:
                StepperDirection = False
                threading.Thread(target=self.spinOtherDirection, args=(button,), daemon=True).start()
            else:
                StepperDirection = True
                threading.Thread(target=self.spinDirection, args=(button,), daemon=True).start()



    def spinDirection(self, button):

        stepper_num = 0
        gear_ratio = 1
        motorStepPerRevolution = 1600 * gear_ratio
        dpiStepper.setStepsPerRevolution(stepper_num, motorStepPerRevolution)

        speed_in_revolutions_per_sec = 2.0
        accel_in_revolutions_per_sec_per_sec = 2.0
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)
        dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(stepper_num, accel_in_revolutions_per_sec_per_sec)

        dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)

        print('starting to turn clockwise')

        waitToFinishFlg = False
        dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 50.0, waitToFinishFlg)

    def spinOtherDirection(self, button):

        stepper_num = 0
        gear_ratio = 1
        motorStepPerRevolution = 1600 * gear_ratio
        dpiStepper.setStepsPerRevolution(stepper_num, motorStepPerRevolution)

        speed_in_revolutions_per_sec = 2.0
        accel_in_revolutions_per_sec_per_sec = 2.0
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)
        dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(stepper_num, accel_in_revolutions_per_sec_per_sec)

        dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)

        print('starting to turn counterclockwise')

        waitToFinishFlg = False
        dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, -50.0, waitToFinishFlg)

    def sliding(self):
        stepper_num = 0
        gear_ratio = 1
        motorStepPerRevolution = 1600 * gear_ratio
        dpiStepper.setStepsPerRevolution(stepper_num, motorStepPerRevolution)

        # Reference the Slider using its ID
        speed_in_revolutions_per_sec = int(self.ids.slider_id.value)
        accel_in_revolutions_per_sec_per_sec = 2.0
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)
        dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(stepper_num, accel_in_revolutions_per_sec_per_sec)

        dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)

        print('speed ' + str(self.ids.slider_id.value))
        waitToFinishFlg = False
        dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 50.0, waitToFinishFlg)

    def danceydance(self):

        dpiStepper.enableMotors(True)

        threading.Thread(target=self.one, daemon=True).start()
        sleep(10)
        threading.Thread(target=self.two, daemon=True).start()
        sleep(8)
        threading.Thread(target=self.three, daemon=True).start()
        sleep(30)
        threading.Thread(target=self.four, daemon=True).start()
        sleep(10)
        threading.Thread(target=self.five, daemon=True).start()

    def one(self):

        currentPosition = dpiStepper.getCurrentPositionInSteps(0)[1]
        print(f"Pos = {currentPosition}")
        sleep(1)

        stepper_num = 0
        gear_ratio = 1
        motorStepPerRevolution = 1600 * gear_ratio
        dpiStepper.setStepsPerRevolution(stepper_num, motorStepPerRevolution)
        speed_in_revolutions_per_sec = 1.0
        accel_in_revolutions_per_sec_per_sec = 2.0
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)
        dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(stepper_num, accel_in_revolutions_per_sec_per_sec)
        dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)

        print('starting 15 turns clockwise')
        print('speed = ' + str(speed_in_revolutions_per_sec))

        waitToFinishFlg = True
        dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 15.0, waitToFinishFlg)

        print(f"Pos = {currentPosition}")
        sleep(1)

        print('sleeping 10 seconds')


    def two(self):

        stepper_num = 0
        gear_ratio = 1
        motorStepPerRevolution = 1600 * gear_ratio
        dpiStepper.setStepsPerRevolution(stepper_num, motorStepPerRevolution)
        speed_in_revolutions_per_sec = 5.0
        accel_in_revolutions_per_sec_per_sec = 2.0
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)
        dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(stepper_num, accel_in_revolutions_per_sec_per_sec)
        dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)

        print('starting 10 turns clockwise')
        print('speed = ' + str(speed_in_revolutions_per_sec))

        waitToFinishFlg = True
        dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 10.0, waitToFinishFlg)

        currentPosition = dpiStepper.getCurrentPositionInSteps(0)[1]
        print(f"Pos = {currentPosition}")
        sleep(1)

        print('sleeping 8 seconds')

    def three(self):

        stepper_num = 0
        gear_ratio = 1
        motorStepPerRevolution = 1600 * gear_ratio
        dpiStepper.setStepsPerRevolution(stepper_num, motorStepPerRevolution)
        speed_in_revolutions_per_sec = 2.0
        accel_in_revolutions_per_sec_per_sec = 2.0
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)
        dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(stepper_num, accel_in_revolutions_per_sec_per_sec)
        dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)

        print('going home')

        dpiStepper.moveToHomeInRevolutions(0, 1, speed_in_revolutions_per_sec, maxDistanceToMoveInRevolutions= 5.0)

        print('sleeping 30 seconds')

    def four(self):

        currentPosition = dpiStepper.getCurrentPositionInSteps(0)[1]
        print(f"Pos = {currentPosition}")
        sleep(1)

        stepper_num = 0
        gear_ratio = 1
        motorStepPerRevolution = 1600 * gear_ratio
        dpiStepper.setStepsPerRevolution(stepper_num, motorStepPerRevolution)
        speed_in_revolutions_per_sec = 8.0
        accel_in_revolutions_per_sec_per_sec = 2.0
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)
        dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(stepper_num, accel_in_revolutions_per_sec_per_sec)
        dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)

        print('starting 100 turns counterclockwise')
        print('speed = ' + str(speed_in_revolutions_per_sec))

        waitToFinishFlg = True
        dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, -100.0, waitToFinishFlg)

        print(f"Pos = {currentPosition}")
        sleep(1)
        print('sleeping 10 seconds')

    def five(self):

        stepper_num = 0
        gear_ratio = 1
        motorStepPerRevolution = 1600 * gear_ratio
        dpiStepper.setStepsPerRevolution(stepper_num, motorStepPerRevolution)

        speed_in_revolutions_per_sec = 1
        accel_in_revolutions_per_sec_per_sec = 2.0
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)
        dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(stepper_num, accel_in_revolutions_per_sec_per_sec)

        dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)

        print('going home')

        dpiStepper.moveToHomeInRevolutions(0, -1, speed_in_revolutions_per_sec, maxDistanceToMoveInRevolutions=1)
        sleep(1)

        currentPosition = dpiStepper.getCurrentPositionInSteps(0)[1]
        print(f"Pos = {currentPosition}")

    def switch(self):
        SCREEN_MANAGER.current = SECOND_SCREEN_NAME

class SecondScreen(Screen):


    def switchback(self):
        SCREEN_MANAGER.current = FIRST_SCREEN_NAME

    def gotothird(self):
        SCREEN_MANAGER.current = THIRD_SCREEN_NAME

    def oneeighty(self):
        dpiComputer = DPiComputer()
        dpiComputer.initialize()

        i = 0
        servo_number = 0
        for i in range(180):
            dpiComputer.writeServo(servo_number, i)
            sleep(.05)

    def zero(self):
        dpiComputer = DPiComputer()
        dpiComputer.initialize()

        i = 0
        servo_number = 0
        for i in range(180, 0, -1):
            dpiComputer.writeServo(servo_number, i)
            sleep(.05)

    def servo_control(self):

        dpiComputer = DPiComputer()
        dpiComputer.initialize()

        value = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)
        dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_2, value)

        value = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)
        dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_2, value)
        while True:
            if (dpiComputer.readDigitalIn(
                    dpiComputer.IN_CONNECTOR__IN_0)):  # binary bitwise AND of the value returned from read.gpio()
                sleep(1)
                if (dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)):  # a little debounce logic
                    print("Input 0 is HIGH")
                    self.oneeighty()
            else:
                print("Input 0 is LOW")
                sleep(1)
                self.zero()

    def terminate(self):

        sleep(1)
        dpiComputer = DPiComputer()
        dpiComputer.initialize()

        print('centering motor')

        i = 0
        servo_number = 0
        for i in range(90):
            dpiComputer.writeServo(servo_number, i)
            sleep(.05)

    def switchcontrol(self):
        # Create a thread for the servo control function
        servo_thread = threading.Thread(target=self.servo_control)
        servo_thread.daemon = True  # Daemonize the thread so it terminates when the main program exits

        # Start the servo control thread
        servo_thread.start()

class ThirdScreen(Screen):

    def Spinny(self):
        dpiComputer = DPiComputer()
        dpiComputer.initialize()

        servo_number = 0
        for i in range(90, 0, -1):
            dpiComputer.writeServo(servo_number, i)
            sleep(20/90)
        dpiComputer.writeServo(0, 90) 

    def limitswitchin(self):
        dpiComputer = DPiComputer()
        dpiComputer.initialize()

        value = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)
        dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_2, value)

        value = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)
        dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_2, value)
        while True:
            if (dpiComputer.readDigitalIn(
                    dpiComputer.IN_CONNECTOR__IN_0)):  # binary bitwise AND of the value returned from read.gpio()
                sleep(1)
                if (dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)):  # a little debounce logic
                    print("Input 0 is HIGH")
                    dpiComputer.writeServo(0, 90)
                else:
                    print("Input 0 is LOW")
                    sleep(1)
                    self.maxcw()

    def maxcw(self):
        dpiComputer = DPiComputer()
        dpiComputer.initialize()

        servo_number = 0
        dpiComputer.writeServo(servo_number, 180)
        sleep(.05)






Builder.load_file('first.kv')
Builder.load_file('second.kv')
Builder.load_file('third.kv')


SCREEN_MANAGER.add_widget(FirstScreen(name=FIRST_SCREEN_NAME))
SCREEN_MANAGER.add_widget(SecondScreen(name=SECOND_SCREEN_NAME))
SCREEN_MANAGER.add_widget(ThirdScreen(name=THIRD_SCREEN_NAME))


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()