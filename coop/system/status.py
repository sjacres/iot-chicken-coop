class Status(object):
    def __init__(self, lcd_plate):
        self._lcd_plate = lcd_plate

    def uptime(self):
        self._lcd_plate.clear()

        self._lcd_plate.message('Uptime Selected')
