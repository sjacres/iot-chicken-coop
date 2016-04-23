from coop.ui.lcdplate import LcdPlate
import pytest

@pytest.fixture()
def lcdplate(request):

    return LcdPlate()