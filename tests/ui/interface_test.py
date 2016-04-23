from coop.ui.interface import UserInterface
import pytest

@pytest.fixture()
def userinterface(request):

    return UserInterface()