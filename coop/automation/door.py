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
        """ Build out an Adafruit Motor Plate Object

        In order to make sure that the motors are off at exit, registers an "at exit" event method to clean up.

        """
        self._lcd_plate = lcd_plate

        if motor_plate is None:
            self._motor_plate = Adafruit_MotorHAT(addr=self.HAT_ADDRESS)
        else:
            self._motor_plate = motor_plate

        self._run_door = self._motor_plate.getMotor(self.RUN_MOTOR_ID)

        self._exterior_door = self._motor_plate.getMotor(self.EXTERIOR_MOTOR_ID)

        # Make sure to clean up when exiting
        atexit.register(self.clean_up)

    def _validate_and_get_door(self, door_name):
        """ Make sure that there is a door with the passed in name & get it

        :param door_name: string The name of the door
        :return: Adafruit_DCMotor
        """
        try:
            return getattr(self, '_' + door_name + '_door')
        except AttributeError:
            self._lcd_plate.clear()
            self._lcd_plate.message('Could not locate\n' + door_name + ' door')

            return None

    def clean_up(self):
        """ Once the script exits, then make sure the motors are off
            """
        for motor_id in range(1, 5):
            self._motor_plate.getMotor(motor_id).run(Adafruit_MotorHAT.RELEASE)

    def close(self, door_name):
        """ Close a door

        :param door_name: string the name of the door to close
        """
        self._lcd_plate.clear()
        self._lcd_plate.message('Closing ' + door_name + '\ndoor...')

        door = self._validate_and_get_door(door_name)

        if door is not None:
            door.run(Adafruit_MotorHAT.BACKWARD)
            door.setSpeed(self.MOTOR_SPEED)
            time.sleep(self.CLOSE_TIME)
            door.run(Adafruit_MotorHAT.RELEASE)

            self._lcd_plate.clear()
            self._lcd_plate.message('Closed ' + door_name + '\ndoor')

    def disable(self, door_name):
        """ Disable the door from auto opening

        :param door_name: string the name of the door to open
        """
        self._lcd_plate.clear()
        self._lcd_plate.message('Disabling ' + door_name + '\ndoor...')

        # TODO: Add code here to disable the automatic doors

        self._lcd_plate.clear()
        self._lcd_plate.message('Disabled ' + door_name + '\ndoor')

    def enable(self, door_name):
        """ Enable the door to auto open

        :param door_name: string the name of the door to open
        """
        self._lcd_plate.clear()
        self._lcd_plate.message('Enabling ' + door_name + '\ndoor...')

        # TODO: Add code here to enable the automatic doors

        self._lcd_plate.clear()
        self._lcd_plate.message('Enabled ' + door_name + '\ndoor')

    def open(self, door_name):
        """ Open a door

        :param door_name: string the name of the door to open
        """
        self._lcd_plate.clear()
        self._lcd_plate.message('Opening ' + door_name + '\ndoor...')

        door = self._validate_and_get_door(door_name)

        if door is not None:
            door.run(Adafruit_MotorHAT.FORWARD)
            door.setSpeed(self.MOTOR_SPEED)
            time.sleep(self.OPEN_TIME)
            door.run(Adafruit_MotorHAT.RELEASE)

            self._lcd_plate.clear()
            self._lcd_plate.message('Opened ' + door_name + '\ndoor')
