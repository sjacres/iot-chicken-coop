from lcdplate import LcdPlate
from navigation import Navigation
import time


class UserInterface(object):
    """ The User Interface to the application

    Boots the application & displays the menu on the LCD for the user to be able to interact with the coop.
    """

    def __init__(self, lcd_plate=None, navigation=None):
        """ Build out a LCD Plate & Navigation object to use with the interface
        """
        if lcd_plate is None:
            self._lcd_plate = LcdPlate()
        else:
            self._lcd_plate = lcd_plate

        if navigation is None:
            self._navigation = Navigation()
        else:
            self._navigation = navigation

        # Track if we are self._asleep
        self._asleep = False

        # Keep up with last screen refresh to know is need to sleep
        self._last_refresh = None

        self._abandon_timeout = 300

    def _read_pressed_button(self):
        """ Checks all of the buttons to see if they are pressed & calls the correct function to deal with the button
        """
        for button in self._lcd_plate.buttons():
            # Check if a button is pressed & there has been pause in pressing the buttons
            if self._lcd_plate.pressed_since_last_check(button):
                # If we just came out of sleep, ignore that button press
                if not self._asleep:
                    # Call function of the button pressed
                    getattr(self, 'pressed_' + self._lcd_plate.title_of_button(button).lower())()

                else:
                    self._asleep = False

                self.refresh()

    def _sleep_if_needed(self):
        """ Puts the interface to "sleep" to lower power consumption when not in use
        """
        if self.abandoned():
            # If we just discovered that we are abandoned, then put the screen to sleep
            if not self._asleep:
                self._lcd_plate.go_to_sleep()

                self._navigation.reset()

                self._asleep = True

            # No reason to poll buttons continuously if asleep, so pause for 5 seconds before checking buttons
            time.sleep(5)

    def abandoned(self):
        """ Looks to if the last interaction was long enough ago to consider that the user is done

        :return:
            bool: True if abandoned, otherwise False
        """
        return self._abandon_timeout <= time.time() - self._last_refresh

    def pressed_down(self):
        """ The down button is pressed, so tell navigation to move down one
        """
        self._navigation.move_down()

    def pressed_left(self):
        """ The left button is pressed, so tell navigation to move back one
        """

        self._navigation.move_left()

    def pressed_right(self):
        """ The right button is pressed, so tell navigation to enter current item
        """

        self._navigation.move_right()

    def pressed_select(self):
        """ The select button is pressed, so process the command for the item
        """

        # TODO: Actually run the process that the navigation items expects
        self._lcd_plate.clear()
        self._lcd_plate.message("In Select")

    def pressed_up(self):
        """ The up button is pressed, so tell navigation to move up one
        """

        self._navigation.move_up()

    def refresh(self):
        """ Put the current navigation item on the screen
        """

        self._lcd_plate.clear()

        self._lcd_plate.set_back_light_cyan()

        # Set the screen to the top of the menu
        self._lcd_plate.message(str(self._navigation.current_item()))

        self._last_refresh = time.time()

    def run(self):
        """ Continuous loop to keep polling to see if any of the buttons are pressed
        """

        self.refresh()

        while True:
            # Check to see if there has been no interaction with the screen for a bit
            self._sleep_if_needed()

            # Loop through the buttons
            self._read_pressed_button()
