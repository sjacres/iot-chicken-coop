import Adafruit_CharLCD as LCD
import atexit


class LcdPlate(object):
    # Make list of button value, text
    _buttons = {
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

    def __init__(self):
        self._lcd_plate = LCD.Adafruit_CharLCDPlate()

        # Make sure to clean up when exiting
        atexit.register(self.cleanUp)

    def beenPressed(self, button):
        return self._buttons[button]['Pressed']

    def buttons(self):
        return self._buttons.keys()

    def cleanUp(self):
        """
        Once the script exits, then clear the screen & turn it off
        """
        self._lcd_plate.clear()
        self._lcd_plate.set_backlight(0)

    def clear(self):
        self._lcd_plate.clear()

    def isPressed(self, button):
        if self._lcd_plate.is_pressed(button):
            self._buttons[button]['Pressed'] = True

            return True

        self._buttons[button]['Pressed'] = False

        return False

    def message(self, text):
        self._lcd_plate.message(text)

    def pressedSinceLastCheck(self, button):
        # Since isPressed will toggle beenPressed, you have to call it first & cache
        been = self.beenPressed(button)
        # Since the first "False" will trigger the second check to not be ran, then cache
        currently = self.isPressed(button)

        return not been and currently

    def setBackLightBlue(self):
        self._lcd_plate.set_color(0.0, 0.0, 1.0)

    def setBackLightCyan(self):
        self._lcd_plate.set_color(0.0, 1.0, 1.0)

    def setBackLightGreen(self):
        self._lcd_plate.set_color(0.0, 1.0, 0.0)

    def setBackLightMagenta(self):
        self._lcd_plate.set_color(1.0, 0.0, 1.0)

    def setBackLightRed(self):
        self._lcd_plate.set_color(1.0, 0.0, 0.0)

    def setBackLightWhite(self):
        self._lcd_plate.set_color(1.0, 1.0, 1.0)

    def setBackLightYellow(self):
        self._lcd_plate.set_color(1.0, 1.0, 0.0)

    def titleOfButton(self, button):
        return self._buttons[button]['Title']
