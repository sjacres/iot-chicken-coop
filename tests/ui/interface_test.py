from mock import Mock, patch
import pytest

# Setup the mock object
MockAdafruit_CharLCD = Mock()


# # Set the values for the constants on the mock object
# MockAdafruit_CharLCD.SELECT = 'SELECT'
# MockAdafruit_CharLCD.LEFT = 'LEFT'
# MockAdafruit_CharLCD.UP = 'UP'
# MockAdafruit_CharLCD.DOWN = 'DOWN'
# MockAdafruit_CharLCD.RIGHT = 'RIGHT'


# @pytest.fixture()
# def mock_lcd():
#     mock = Mock()
#
#     return mock

@pytest.fixture()
def mock_lcd_plate():
    return Mock()


@pytest.fixture()
def mock_navigation():
    return Mock()


@pytest.fixture()
@patch.dict('sys.modules', Adafruit_CharLCD=MockAdafruit_CharLCD)
def interface(mock_lcd_plate, mock_navigation):
    # Do import at this place, so that the patch will catch the mocked class
    from coop.ui.interface import UserInterface

    return UserInterface(mock_lcd_plate, mock_navigation)


def test_first(interface):
    assert True == True
