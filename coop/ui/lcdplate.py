import Adafruit_CharLCD as LCD
import atexit


class LcdPlate(object):
    """ Wrapper of Adafruit's LCD library

    Add some sugar to the Adafruit library to make interacting with the plate a little easier
    """

    def __init__(self, lcd_plate=None):
        """ Build out an Adafruit LCD Plate Object

        In order to clean up the display on exit of the object, registers an "at exit" event method to clean up.

        """

        if None == lcd_plate:
            self._lcd_plate = LCD.Adafruit_CharLCDPlate()
        else:
            self._lcd_plate = lcd_plate

        # Make list of button value, text
        self._buttons = {
            LCD.SELECT: {
                'Pressed': False,
                'Title': 'Select',
            },
            LCD.LEFT: {
                'Pressed': False,
                'Title': 'Left',
            },
            LCD.UP: {
                'Pressed': False,
                'Title': 'Up',
            },
            LCD.DOWN: {
                'Pressed': False,
                'Title': 'Down',
            },
            LCD.RIGHT: {
                'Pressed': False,
                'Title': 'Right',
            },
        }

        # Make sure to clean up when exiting
        atexit.register(self.cleanUp)

    def beenPressed(self, button):
        """ Check to see if the button was down the last time it was checked

        :param button:
            int: The id of the button

        :return:
            bool: True if it was down last check, or False if it was not
        """
        return self._buttons[button]['Pressed']

    def buttons(self):
        """ Get the ID's of the buttons

        Each button has a unique ID, so this is a list of those buttons

        :return:
            list: List of the ID's of the buttons
        """
        return self._buttons.keys()

    def cleanUp(self):
        """ Once the script exits, then clear the screen & turn it off
        """
        self.clear()
        self.turnOffBackLight()

    def clear(self):
        """ Clear the screen
        """
        self._lcd_plate.clear()

    def goToSleep(self):
        """ Put the screen asleep

        Turn off the back light & display a message to press any button to wake it up
        """
        self.clear()
        self._lcd_plate.message("Sleeping...\nHold any button")
        self.turnOffBackLight()

    def isPressed(self, button):
        """ Check to see if the passed in button is pressed

        Since there is no way to know if a person is holding the button down from the Adafruit library, we keep up the
        last status that it was when we checked for it.

        :param button:
            int: Id of the button to see if it is down

        :return:
            bool: True if the button is down, otherwise False
        """
        if self._lcd_plate.is_pressed(button):
            self._buttons[button]['Pressed'] = True

            return True

        self._buttons[button]['Pressed'] = False

        return False

    def message(self, text):
        """ Display the string on the display

        Use new line \n to wrap the text to the second line

        :param text:
            string: The text to display on the display
        """
        self._lcd_plate.message(text)

    def pressedSinceLastCheck(self, button):
        """ Has the button been pressed since last check

        There is no event from the Adafruit library that lets you know when a button was pressed, so you have to poll
        the plate asking it if the button is down.  That means that there is not a good way to know if the user is
        just holding the button down.

        :param button:
            int: Id of the button to see if it is down

        :return:
            bool: True if was not pressed last check, but pressed this time, otherwise, False
        """
        # Since isPressed will toggle beenPressed, you have to call it first & cache
        been = self.beenPressed(button)
        # Since the first "False" will trigger the second check to not be ran, then cache
        currently = self.isPressed(button)

        return not been and currently

    def setBackLightBlue(self):
        """ Set the back light to blue.
        """
        self._lcd_plate.set_color(0.0, 0.0, 1.0)

    def setBackLightCyan(self):
        """ Set the back light to cyan.
        """
        self._lcd_plate.set_color(0.0, 1.0, 1.0)

    def setBackLightGreen(self):
        """ Set the back light to green.
        """
        self._lcd_plate.set_color(0.0, 1.0, 0.0)

    def setBackLightMagenta(self):
        """ Set the back light to magenta.
        """
        self._lcd_plate.set_color(1.0, 0.0, 1.0)

    def setBackLightRed(self):
        """ Set the back light to red.
        """
        self._lcd_plate.set_color(1.0, 0.0, 0.0)

    def setBackLightWhite(self):
        """ Set the back light to white.
        """
        self._lcd_plate.set_color(1.0, 1.0, 1.0)

    def setBackLightYellow(self):
        """ Set the back light to yellow.
        """
        self._lcd_plate.set_color(1.0, 1.0, 0.0)

    def titleOfButton(self, button):
        return self._buttons[button]['Title']

    def turnOffBackLight(self):
        """ Turn off the back light.
        """
        self._lcd_plate.set_backlight(0)
