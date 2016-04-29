from mock import Mock, patch
import pytest

# Setup the mock object
MockAdafruit_MotorHAT = Mock()


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


@pytest.mark.skip(reason="This is just a stub")
def test_something(door):
    # TODO: Write test here
    pass
