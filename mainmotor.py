
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

import threading
from time import sleep

time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
FIRST_SCREEN_NAME = 'first'

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

    def danceydance(self, button):

        dpiStepper.enableMotors(True)

        currentPosition = dpiStepper.getCurrentPositionInSteps(0)[1]
        print(f"Pos = {currentPosition}")
        sleep(1)

        threading.Thread(target=self.one, args=(button,), daemon=True).start()
        threading.Thread(target=self.two, args=(button,), daemon=True).start()


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

        waitToFinishFlg = False
        dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 15.0, waitToFinishFlg)

        print('sleeping 10 seconds')
        sleep(10)


    def two(self):

        currentPosition = dpiStepper.getCurrentPositionInSteps(0)[1]
        print(f"Pos = {currentPosition}")
        sleep(1)

        stepper_num = 0
        gear_ratio = 1
        motorStepPerRevolution = 1600 * gear_ratio
        dpiStepper.setStepsPerRevolution(stepper_num, motorStepPerRevolution)

        speed_in_revolutions_per_sec = 5
        accel_in_revolutions_per_sec_per_sec = 2.0
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)
        dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(stepper_num, accel_in_revolutions_per_sec_per_sec)

        dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)

        print('starting 10 turns clockwise')
        print('speed = ' + str(speed_in_revolutions_per_sec))

        waitToFinishFlg = False
        dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 15.0, waitToFinishFlg)

        print('sleeping 8 seconds')
        sleep(8)

    def three(self):
        pass





Builder.load_file('first.kv')
SCREEN_MANAGER.add_widget(FirstScreen(name=FIRST_SCREEN_NAME))

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