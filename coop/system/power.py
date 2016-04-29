class Power(object):
    def __init__(self, lcd_plate):
        self._lcd_plate = lcd_plate

    def reboot(self):
        self._lcd_plate.clear()

        self._lcd_plate.message('Reboot Selected')

    def shutdown(self):
        self._lcd_plate.clear()

        self._lcd_plate.message('Shutdown Selected')
