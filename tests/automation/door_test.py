from coop.automation.door import Door
from mock import Mock
import pytest


@pytest.fixture()
def mock_lcd_plate():
    return Mock()


@pytest.fixture()
def door(mock_lcd_plate):
    return Door(mock_lcd_plate)


def test_it_can_be_constructed(door):
    assert isinstance(door, Door)


@pytest.mark.skip(reason="This is just a stub")
def test_something(door):
    # TODO: Write test here
    pass
