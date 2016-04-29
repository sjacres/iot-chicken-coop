class Door(object):
    def __init__(self, lcd_plate):
        self._lcd_plate = lcd_plate

    def close(self, door):
        print door
        self._lcd_plate.clear()

        self._lcd_plate.message('Close Selected for\n ' + door + " door")

    def disable(self, door):
        print door
        self._lcd_plate.clear()

        self._lcd_plate.message('Disable Selected for\n ' + door + " door")

    def enable(self, door):
        print door
        self._lcd_plate.clear()

        self._lcd_plate.message('Enable Selected for\n ' + door + " door")

    def open(self, door):
        print door
        self._lcd_plate.clear()

        self._lcd_plate.message('Open Selected for\n ' + door + " door")
