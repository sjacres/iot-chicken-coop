from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit


class Door(object):
    CLOSE_TIME = 2.5
    HAT_ADDRESS = 0x60
    RUN_MOTOR_ID = 1
    EXTERIOR_MOTOR_ID = 2
    MOTOR_SPEED = 150
    OPEN_TIME = 3

    def __init__(self, lcd_plate, motor_plate=None):
        self._lcd_plate = lcd_plate

        if motor_plate is None:
            self._motor_plate = Adafruit_MotorHAT(addr=self.HAT_ADDRESS)
        else:
            self._motor_plate = motor_plate

        self._run_door = self._motor_plate.getMotor(self.RUN_MOTOR_ID)

        self._external_door = self._motor_plate.getMotor(self.EXTERIOR_MOTOR_ID)

        # Make sure to clean up when exiting
        atexit.register(self.clean_up)

    def clean_up(self):
        """ Once the script exits, then make sure the motors are off
            """
        for motor_id in range(1, 4):
            self._motor_plate.getMotor(motor_id).run(Adafruit_MotorHAT.RELEASE)

    def close(self, door):
        print door
        self._lcd_plate.clear()

        self._lcd_plate.message('Close Selected for\n ' + door + " door")

        # .run(Adafruit_MotorHAT.BACKWARD)
        # .setSpeed(self.MOTOR_SPEED)
        time.sleep(self.CLOSE_TIME)
        # .run(Adafruit_MotorHAT.RELEASE)

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

        # .run(Adafruit_MotorHAT.FORWARD)
        # .setSpeed(self.MOTOR_SPEED)
        time.sleep(self.OPEN_TIME)
        # .run(Adafruit_MotorHAT.RELEASE)
