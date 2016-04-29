from coop.system.status import Status
from mock import Mock
import pytest


@pytest.fixture()
def mock_lcd_plate():
    return Mock()


@pytest.fixture()
def status(mock_lcd_plate):
    return Status(mock_lcd_plate)


def test_it_can_be_constructed(status):
    assert isinstance(status, Status)


@pytest.mark.skip(reason="This is just a stub")
def test_something(status):
    # TODO: Write test here
    pass
