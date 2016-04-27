from lcdplate import LcdPlate
from navigation import Navigation
import time


class UserInterface(object):
    """ The User Interface to the application

    Boots the application & displays the menu on the LCD for the user to be able to interact with the coop.
    """

    def __init__(self, lcd_plate = None, navigation = None):
        """ Build out a LCD Plate & Navigation object to use with the interface
        """
        if None == lcd_plate:
            self._lcd_plate = LcdPlate()
        else:
            self._lcd_plate = lcd_plate

        if None == navigation:
            self._navigation = Navigation()
        else:
            self._navigation = navigation

    def _readPressedButton(self):
        """ Checks all of the buttons to see if they are pressed & calls the correct function to deal with the button
        """
        for button in self._lcd_plate.buttons():
            # Check if a button is pressed & there has been pause in pressing the buttons
            if self._lcd_plate.pressedSinceLastCheck(button):
                # If we just came out of sleep, ignore that button press
                if not self._asleep:
                    # Call function of the button pressed
                    getattr(self, 'pressed' + self._lcd_plate.titleOfButton(button))()

                else:
                    self._asleep = False

                self.refresh()

    def _sleepIfNeeded(self):
        """ Puts the interface to "sleep" to lower power consumption when not in use
        """
        if self.abandoned():
            # If we just discovered that we are abandoned, then put the screen to sleep
            if not self._asleep:
                self._lcd_plate.goToSleep()

                self._navigation.reset()

                self._asleep = True

            # No reason to poll buttons continuously if asleep, so pause for 5 seconds before checking buttons
            time.sleep(5)

    def abandoned(self):
        """ Looks to if the last interaction was long enough ago to consider that the user is done

        :return:
            bool: True if abandoned, otherwise False
        """
        return 300 <= time.time() - self._last_refresh

    def pressedDown(self):
        """ The down button is pressed, so tell navigation to move down one
        """
        self._navigation.moveDown()

    def pressedLeft(self):
        """ The left button is pressed, so tell navigation to move back one
        """

        self._navigation.moveLeft()

    def pressedRight(self):
        """ The right button is pressed, so tell navigation to enter current item
        """

        self._navigation.moveRight()

    def pressedSelect(self):
        """ The select button is pressed, so process the command for the item
        """

        # TODO: Actually run the process that the navigation items expects
        self._lcd_plate.clear()
        self._lcd_plate.message("In Select")

    def pressedUp(self):
        """ The up button is pressed, so tell navigation to move up one
        """

        self._navigation.moveUp()

    def refresh(self):
        """ Put the current navigation item on the screen
        """

        self._lcd_plate.clear()

        self._lcd_plate.setBackLightCyan()

        # Set the screen to the top of the menu
        self._lcd_plate.message(str(self._navigation.currentItem()))

        # self._last_refresh = time.time()

    def run(self):
        """ Continuous loop to keep polling to see if any of the buttons are pressed
        """

        # Track if we are self._asleep
        self._asleep = False

        self.refresh()

        while True:
            # Check to see if there has been no interaction with the screen for a bit
            self._sleepIfNeeded()

            # Loop through the buttons
            self._readPressedButton()
