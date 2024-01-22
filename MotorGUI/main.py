
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



time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
NEW_SCREEN_NAME = 'newscreen'
JOYSTICK_SCREEN_NAME = 'joystickscreen'

Builder.load_file('newscreen.kv')
Builder.load_file('joystick.kv')

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


Window.clearcolor = (.132, .156, .194, 1)  # White

button_toggle = False



class MainScreen(Screen):

    press_count = NumericProperty(0)
    """
    Class to handle the main screen and its associated touch events
    """
    def pressed(self, button):
        """f
        Function called on button touch event for button with id: testButton
        :return: None
        """
        global button_toggle
        self.press_count += 1


        print("Callback from MainScreen.pressed()")

        if button_toggle == False:
            button_toggle = True
            button.text = ''

        else:
            button_toggle = False
            button.text = 'yo mama'

    def update_press_count(self):
        return self.press_count
    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'

    def animation(self, button):
        anim = Animation(x = 100, y = 100) + Animation(size=(80, 80), duration = 2.)
        anim.bind(on_complete=lambda *args: setattr(SCREEN_MANAGER, 'current', NEW_SCREEN_NAME))
        anim.start(button)

    def transition(self, button):
        SCREEN_MANAGER.current = JOYSTICK_SCREEN_NAME



class NewScreen(Screen):
    def goback(self, button):
        anim = Animation(x=50) + Animation(size=(80, 80), t='in_quad')
        anim.bind(on_complete=lambda *args: setattr(SCREEN_MANAGER, 'current', MAIN_SCREEN_NAME))
        anim.start(button)
class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """
    def print2(self):
        print("switched")
    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)
    joy = Joystick(0, True)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()

class JoystickScreen(Screen):
    joy = Joystick(0, False)

    def __init__(self, **kwargs):
        super(JoystickScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_button_text, 0.1)

    def update_button_text(self, dt):
        if  -0.0001 <= self.joy.get_axis('y') >= -0.0001:
            self.ids.joystick_button.text = str(self.joy.get_axis('x')) + ', 0.0'
        elif -0.0001 <= self.joy.get_axis('x') >= -0.0001:
            self.ids.joystick_button.text = '0.0, ' + str(self.joy.get_axis('y'))
        elif 0.99 <= self.joy.get_axis('x') >= 1:
            self.ids.joystick_button.text = '1.0, ' + str(self.joy.get_axis('y'))
        else:
            self.ids.joystick_button.text = str(self.joy.get_axis('x')) + ', ' + str(self.joy.get_axis('y'))


        pressed_button = None
        for button_num in range(11):
            if self.joy.get_button_state(button_num):
                pressed_button = button_num + 1  # Adjust button number to be 1-indexed
                break

        # Set the text of joystick_buttonss based on the pressed button
        self.ids.joystick_buttonss.text = str(pressed_button) if pressed_button is not None else ''

    def transitionback(self, button):
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    def update_other_button(self, dt):
        self.ids.joystick_buttonss.text = str(self.joystick.get_button(button_num))

class Joystick:
    """
    Class to handle the joystick and getting current states
    """

    def __init__(self, number, ssh_deploy):
        """
        Initialize Joystick
        :param number: Joystick number
        :param ssh_deploy: True if deploying over ssh
        """
        if ssh_deploy:  # allow ssh deploy with pygame
            os.environ['SDL_VIDEODRIVER'] = "dummy"

        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(number)
        self.joystick.init()

        self.num_buttons = self.joystick.get_numbuttons()

    def get_axis(self, axis):
        """
        Get the axis (x or y) of the joystick.
        :raises: ValueError If the given axis isn't 'x' 'y'
        :param axis: axis to get value of
        :rtype: float
        :return: All the way to the right=1, fully up=-1
        """
        axis.lower()
        self.refresh()

        if axis == 'x':
            return self.joystick.get_axis(0)
        elif axis == 'y':
            return self.joystick.get_axis(1)

        else:
            raise ValueError("Axis must be of type str and either 'x' or 'y'")

    def get_both_axes(self):
        """
        Get the status of both axes (x and y)
        :return: An array of both axes, [x-axis, y-axis]
        """
        return [self.get_axis('x'), self.get_axis('y')]

    def get_button_state(self, button_num):
        """
        Get the state of a button. This project uses the "Logitech Attack 3" which contains 11 physical buttons but are
        indexed 0-10
        :param button_num: Button number to get the state of
        :raises: ValueError if the given button number is not in the range of available buttons
        :rtype: int
        :return: 0 or 1 (1=button depressed)
        """
        self.refresh()

        if button_num not in range(self.num_buttons):
            raise ValueError("The button number given is not a button on the joystick, "
                             "must be in range (0-%s)" % self.num_buttons)
        else:
            return self.joystick.get_button(button_num)

    def button_combo_check(self, buttons):
        """
        Check to see if the given button numbers are all being pressed
        :param buttons: List of buttons to check
        :rtype: bool
        :return: True if ALL of the buttons are being pressed, false otherwise
        """
        self.refresh()

        for button in buttons:
            if not self.get_button_state(button):
                return False
        return True
    @staticmethod
    def refresh():
        """
        Refresh the joysticks current value
        :return: None
        """
        pygame.event.pump()

    def get_button_state(self, button_num):
        """
        Get the state of a button. This project uses the "Logitech Attack 3" which contains 11 physical buttons but are
        indexed 0-10
        :param button_num: Button number to get the state of
        :raises: ValueError if the given button number is not in the range of available buttons
        :rtype: int
        :return: 0 or 1 (1=button depressed)
        """
        self.refresh()

        if button_num not in range(self.num_buttons):
            raise ValueError("The button number given is not a button on the joystick, "
                             "must be in range (0-%s)" % self.num_buttons)
        else:
            return self.joystick.get_button(button_num)

    def button_combo_check(self, buttons):
        """
        Check to see if the given button numbers are all being pressed
        :param buttons: List of buttons to check
        :rtype: bool
        :return: True if ALL of the buttons are being pressed, false otherwise
        """
        self.refresh()

        for button in buttons:
            if not self.get_button_state(button):
                return False
        return True


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))

SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(NewScreen(name=NEW_SCREEN_NAME))
SCREEN_MANAGER.add_widget(JoystickScreen(name=JOYSTICK_SCREEN_NAME))

"""
MixPanel
"""


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
