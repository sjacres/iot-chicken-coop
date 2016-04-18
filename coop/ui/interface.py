from lcdplate import LcdPlate
from navigation import Navigation
import time


class Interface(object):
    def __init__(self):
        self._lcd_plate = LcdPlate()

        self._navigation = Navigation()

    def _readPressedButton(self):
        for button in self._lcd_plate.buttons():
            print "Checking button ]" + str(button) + "["
            # Check if a button is pressed & there has been pause in pressing the buttons
            if self._lcd_plate.pressedSinceLastCheck(button):
                print "New press"
                # If we just came out of sleep, ignore that button press
                if not self._asleep:
                    print "Was not asleep"
                    # Call function of the button pressed
                    getattr(self, 'pressed' + self._lcd_plate.titleOfButton(button))()

                else:
                    print "Just woke up"
                    self._asleep = False

                self.refresh()

    def _sleepIfNeeded(self):
        if self.abandoned():
            print "Not abandoned"

            # If we just discovered that we are abandoned, then put the screen to sleep
            if not self._asleep:
                print "Just went to sleep"

                self._lcd_plate.goToSleep()

                self._navigation.reset()

                self._asleep = True

            print "sleeping"
            # No reason to poll buttons continuously if asleep, so pause for 5 seconds before checking buttons
            time.sleep(5)

    def abandoned(self):
        return 300 <= time.time() - self._last_refresh

    def pressedDown(self):
        self._navigation.moveDown()

    def pressedLeft(self):
        self._navigation.moveLeft()

    def pressedRight(self):
        self._navigation.moveRight()

    def pressedSelect(self):
        # TODO: Actually run the process that the navigation items expects
        self._lcd_plate.clear()
        self._lcd_plate.message("In Select")

    def pressedUp(self):
        self._navigation.moveUp()

    def refresh(self):
        self._lcd_plate.clear()

        self._lcd_plate.setBackLightCyan()

        # Set the screen to the top of the menu
        self._lcd_plate.message(self._navigation.currentItem())

        self._last_refresh = time.time()

    def run(self):
        # Track if we are self._asleep
        self._asleep = False

        self.refresh()

        # Continuous loop to keep polling to see if any of the buttons are pressed
        while True:
            # Check to see if there has been no interaction with the screen for a bit
            self._sleepIfNeeded()

            # Loop through the buttons
            self._readPressedButton()
