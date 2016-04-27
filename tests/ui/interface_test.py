from mock import Mock, patch
import pytest
import time

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


# mock_time = Mock(spec=time)
# mock_time.time.return_value = 600


# @patch('time.time', mock_time)
# @patch.dict('sys.modules', Adafruit_CharLCD=MockAdafruit_CharLCD)
@pytest.mark.skip(reason="Cannot figure out how to mock time to make the 5 min spread")
@patch('interface.time.time')
# TODO: This needs to be fixed in "test_that_refresh_puts_the_display_in_correct_state" below
# TODO: This needs to be fixed in "test_run_puts_application_in_running_state" below
def test_it_knows_that_the_user_abandoned_the_interface(interface):
    # Do import at this place, so that the patch will catch the mocked class
    # from coop.ui.interface import UserInterface

    interface._last_refresh = 300
    interface.time.time.time.return_value = 600

    # print "interface.time.time.time = ]" + str(interface.time.time()) + "["

    # assert True == False

    assert True == interface.abandoned()


def test_when_the_down_button_is_pressed_navigation_is_informed(interface):
    interface.pressed_down()

    interface._navigation.move_down.assert_called_once_with()


def test_when_the_left_button_is_pressed_navigation_is_informed(interface):
    interface.pressed_left()

    interface._navigation.move_left.assert_called_once_with()


def test_when_the_right_button_is_pressed_navigation_is_informed(interface):
    interface.pressed_right()

    interface._navigation.move_right.assert_called_once_with()

@pytest.mark.skip(reason="Have not really wired up this call, so skipping for now")
def test_when_the_select_button_is_pressed_navigation_is_informed(interface):
    interface.pressed_select()

    # interface._navigation.moveSelect.assert_called_once_with()


def test_when_the_up_button_is_pressed_navigation_is_informed(interface):
    interface.pressed_up()

    interface._navigation.move_up.assert_called_once_with()

@pytest.mark.skip(reason="Cannot figure out how to mock time to make the 5 min spread")
# TODO: This needs to be fixed in "test_it_knows_that_the_user_abandoned_the_interface" above
# TODO: This needs to be fixed in "test_run_puts_application_in_running_state" below
def test_that_refresh_puts_the_display_in_correct_state(interface):
    interface.refresh()

    interface._lcd_plate.clear.assert_called_once_with()

    interface._lcd_plate.set_back_light_cyan.assert_called_once_with()

    current_item = "Current Item"

    interface._navigation.currentitem.return_value = current_item

    interface._lcd_plate.message.assert_called_once_with(current_item)

@pytest.mark.skip(reason="Cannot figure out how to mock time to make the 5 min spread")
# TODO: This needs to be fixed in "test_it_knows_that_the_user_abandoned_the_interface" above
# TODO: This needs to be fixed in "test_that_refresh_puts_the_display_in_correct_state" above
def test_run_puts_application_in_running_state(interface):
    pass