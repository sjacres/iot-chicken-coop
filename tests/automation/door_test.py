from mock import Mock, patch
import pytest

# Setup the mock object
MockAdafruit_MotorHAT = Mock()
# Set the values for the constants on the mock object
MockAdafruit_MotorHAT.BACKWARD = 'Backward'
MockAdafruit_MotorHAT.FORWARD = 'Forward'
MockAdafruit_MotorHAT.RELEASE = 'Release'

# TODO: Fix the error on the atexit issue where the AdaFruit_MotorHAT is NoneType, so showing error
# AttributeError: 'NoneType' object has no attribute 'RELEASE'


@pytest.fixture()
def mock_lcd_plate():
    return Mock()


@pytest.fixture()
def mock_motor_plate():
    return Mock()


# Intercept the import in the LcdPlate since module may not even be available
@patch.dict('sys.modules', Adafruit_MotorHAT=MockAdafruit_MotorHAT)
@pytest.fixture()
def door(mock_lcd_plate, mock_motor_plate):
    from coop.automation.door import Door

    return Door(mock_lcd_plate, mock_motor_plate)


@pytest.mark.skip(reason="Figure out why this assertion fails")
# assert isinstance(<coop.automation.door.Door object at 0x11035cb50>, <class 'coop.automation.door.Door'>)
# Intercept the import in the LcdPlate since module may not even be available
@patch.dict('sys.modules', Adafruit_MotorHAT=MockAdafruit_MotorHAT)
def test_it_can_be_constructed(door):
    from coop.automation.door import Door

    assert isinstance(door, Door)


def test_clean_up_stops_all_of_the_motors(door):
    door.clean_up()

    door._motor_plate.getMotor.assert_any_call(1)
    door._motor_plate.getMotor.assert_any_call(2)
    door._motor_plate.getMotor.assert_any_call(3)
    door._motor_plate.getMotor.assert_any_call(4)

    # TODO: Test that "Release was called"


def test_that_close_runs_the_correct_motor_in_the_correct_direction_while_displaying_expected_message(door):
    door.close('exterior')

    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_any_call('Closing exterior\ndoor...')

    # door._exterior_door.run.assert_any_call('Backward')
    # door._exterior_door.setSpeed.assert_called_once_with(150)
    # # TODO: Verify length of time
    # door._exterior_door.run.assert_called_with('Release')

    door._lcd_plate.message.assert_called_with('Closed exterior\ndoor')

    door.close('run')

    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_any_call('Closing run\ndoor...')

    # door._run_door.run.assert_any_call('Backward')
    # door._run_door.setSpeed.assert_called_once_with(150)
    # # TODO: Verify length of time
    # door._run_door.run.assert_called_with('Release')

    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_called_with('Closed run\ndoor')


def test_that_opens_runs_the_correct_motor_in_the_correct_direction_while_displaying_expected_message(door):
    door.open('exterior')

    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_any_call('Opening exterior\ndoor...')

    # door._exterior_door.run.assert_any_call('Forward')
    # door._exterior_door.setSpeed.assert_called_once_with(150)
    # # TODO: Verify length of time
    # door._exterior_door.run.assert_called_with('Release')

    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_called_with('Opened exterior\ndoor')

    door.open('run')

    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_any_call('Opening run\ndoor...')

    # door._run_door.run.assert_any_call('Forward')
    # door._run_door.setSpeed.assert_called_once_with(150)
    # # TODO: Verify length of time
    # door._run_door.run.assert_called_with('Release')

    door._lcd_plate.message.assert_called_with('Opened run\ndoor')

def test_that_an_error_is_displayed_on_the_screen_for_an_invalid_door_name(door):
    door.close('fake')

    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_any_call('Closing fake\ndoor...')
    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_any_call('Could not locate\nfake door')

    door.open('fake')

    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_any_call('Opening fake\ndoor...')
    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_any_call('Could not locate\nfake door')


def test_that_disable_marks_the_correct_door_as_disabled_while_displaying_expected_message(door):
    door.disable('exterior')

    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_any_call('Disabling exterior\ndoor...')

    # TODO: Test the disable once we code it out

    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_called_with('Disabled exterior\ndoor')

    door.disable('run')

    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_any_call('Disabling run\ndoor...')

    # TODO: Test the disable once we code it out

    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_called_with('Disabled run\ndoor')


def test_that_enable_marks_the_correct_door_as_enabled_while_displaying_expected_message(door):
    door.enable('exterior')

    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_any_call('Enabling exterior\ndoor...')

    # TODO: Test the disable once we code it out

    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_called_with('Enabled exterior\ndoor')

    door.enable('run')

    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_any_call('Enabling run\ndoor...')

    # TODO: Test the disable once we code it out

    door._lcd_plate.clear.assert_any_call()
    door._lcd_plate.message.assert_called_with('Enabled run\ndoor')
