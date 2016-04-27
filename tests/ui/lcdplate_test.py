from mock import Mock, patch
import pytest

# Setup the mock object
MockAdafruit_CharLCD = Mock()
# Set the values for the constants on the mock object
MockAdafruit_CharLCD.SELECT = 'SELECT'
MockAdafruit_CharLCD.LEFT = 'LEFT'
MockAdafruit_CharLCD.UP = 'UP'
MockAdafruit_CharLCD.DOWN = 'DOWN'
MockAdafruit_CharLCD.RIGHT = 'RIGHT'


@pytest.fixture()
def mock_lcd():
    mock = Mock()

    return mock


# Intercept the import in the LcdPlate since module may not even be available
@patch.dict('sys.modules', Adafruit_CharLCD=MockAdafruit_CharLCD)
@pytest.fixture()
def lcdplate(mock_lcd):
    # Do import at this place, so that the patch will catch the mocked class
    from coop.ui.lcdplate import LcdPlate

    return LcdPlate(mock_lcd)


def test_knowing_if_a_button_has_been_previously_pressed(lcdplate):
    lcdplate._buttons['SELECT']['Pressed'] = True

    assert True == lcdplate.been_pressed('SELECT')


def test_returning_the_button_ids(lcdplate):
    assert ['DOWN', 'RIGHT', 'UP', 'SELECT', 'LEFT'] == lcdplate.buttons()


def test_cleaning_the_screen_clears_it_and_turns_off_backlight(lcdplate):
    lcdplate.clean_up()

    lcdplate._lcd_plate.clear.assert_called_once_with()
    lcdplate._lcd_plate.set_backlight.assert_called_once_with(0)


def test_clearing_the_screen_tells_the_plate_to_clear(lcdplate):
    lcdplate.clear()

    lcdplate._lcd_plate.clear.assert_called_once_with()


def test_going_to_sleep(lcdplate):
    lcdplate.go_to_sleep()

    lcdplate._lcd_plate.clear.assert_called_once_with()
    lcdplate._lcd_plate.message.assert_called_once_with("Sleeping...\nHold any button")
    lcdplate._lcd_plate.set_backlight.assert_called_once_with(0)


def test_it_knows_if_a_button_is_currently_pressed_and_caches_it(lcdplate):
    lcdplate._lcd_plate.is_pressed.return_value = True

    assert False == lcdplate._buttons['SELECT']['Pressed']
    assert True == lcdplate.is_pressed('SELECT')
    assert True == lcdplate._buttons['SELECT']['Pressed']


def test_it_know_if_a_button_is_not_pressed_and_clears_out_the_cache(lcdplate):
    lcdplate._lcd_plate.is_pressed.return_value = False
    lcdplate._buttons['SELECT']['Pressed'] = True

    assert True == lcdplate._buttons['SELECT']['Pressed']
    assert False == lcdplate.is_pressed('SELECT')
    assert False == lcdplate._buttons['SELECT']['Pressed']


def test_that_it_displays_a_message(lcdplate):
    lcdplate.message("Test")

    lcdplate._lcd_plate.message.assert_called_once_with('Test')


def test_it_ignores_a_button_that_is_just_held_down(lcdplate):
    lcdplate._lcd_plate.is_pressed.return_value = True
    lcdplate._buttons['SELECT']['Pressed'] = True

    assert False == lcdplate.pressed_since_last_check('SELECT')


def test_sets_the_back_light_to_blue(lcdplate):
    lcdplate.set_back_light_blue()

    lcdplate._lcd_plate.set_color.assert_called_once_with(0.0, 0.0, 1.0)


def test_sets_the_back_light_to_cyan(lcdplate):
    lcdplate.set_back_light_cyan()

    lcdplate._lcd_plate.set_color.assert_called_once_with(0.0, 1.0, 1.0)


def test_sets_the_back_light_to_green(lcdplate):
    lcdplate.set_back_light_green()

    lcdplate._lcd_plate.set_color.assert_called_once_with(0.0, 1.0, 0.0)


def test_sets_the_back_light_to_magenta(lcdplate):
    lcdplate.set_back_light_magenta()

    lcdplate._lcd_plate.set_color.assert_called_once_with(1.0, 0.0, 1.0)


def test_sets_the_back_light_to_red(lcdplate):
    lcdplate.set_back_light_red()

    lcdplate._lcd_plate.set_color.assert_called_once_with(1.0, 0.0, 0.0)


def test_sets_the_back_light_to_white(lcdplate):
    lcdplate.set_back_light_white()

    lcdplate._lcd_plate.set_color.assert_called_once_with(1.0, 1.0, 1.0)


def test_sets_the_back_light_to_yellow(lcdplate):
    lcdplate.set_back_light_yellow()

    lcdplate._lcd_plate.set_color.assert_called_once_with(1.0, 1.0, 0.0)


def test_it_returns_the_title_of_a_button(lcdplate):
    assert 'Select' == lcdplate.title_of_button('SELECT')
    assert 'Left' == lcdplate.title_of_button('LEFT')
    assert 'Up' == lcdplate.title_of_button('UP')
    assert 'Down' == lcdplate.title_of_button('DOWN')
    assert 'Right' == lcdplate.title_of_button('RIGHT')


def test_that_the_back_light_can_be_turned_off(lcdplate):
    lcdplate.turn_off_back_light()

    lcdplate._lcd_plate.set_backlight.assert_called_once_with(0)
