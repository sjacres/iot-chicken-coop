from lcdplate import LcdPlate
from navigation import Navigation


class Interface(object):
    def __init__(self):
        self._lcd_plate = LcdPlate()

        self._navigation = Navigation()

        self.initScreen()

    def initScreen(self):
        self._lcd_plate.clear()

        self._lcd_plate.setBackLightCyan()

        # Set the screen to the top of the menu
        self._lcd_plate.message(self._navigation.currentItem())

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

    def run(self):
        while True:
            for button in self._lcd_plate.buttons():
                # Check if a button is pressed & there has been pause in pressing the buttons
                if self._lcd_plate.pressedSinceLastCheck(button):
                    # Call function of the button pressed
                    getattr(self, 'pressed' + self._lcd_plate.titleOfButton(button))()

                    self.initScreen()
