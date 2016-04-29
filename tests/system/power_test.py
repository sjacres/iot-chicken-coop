from coop.system.power import Power
from mock import Mock
import pytest


@pytest.fixture()
def mock_lcd_plate():
    return Mock()


@pytest.fixture()
def power(mock_lcd_plate):
    return Power(mock_lcd_plate)


def test_it_can_be_constructed(power):
    assert isinstance(power, Power)


@pytest.mark.skip(reason="This is just a stub")
def test_something(power):
    # TODO: Write test here
    pass
